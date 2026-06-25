"""
Bundles a multi-file Python project into a single file for VEX V5 VS Code,
which only supports one source file. Walks main.py, finds local imports
(modules that exist as .py files in the same directory), and inlines them
recursively. Imports that aren't local files (vex, urandom, etc.) are left
untouched.
"""

from pathlib import Path
import re

# "import foo" / "import foo as bar" / "import foo, baz"
IMPORT_RE = re.compile(r"^import\s+(.+)$")
# "from foo import bar" / "from foo.bar import baz" / "from .foo import bar"
FROM_IMPORT_RE = re.compile(r"^from\s+(\.+\w[\w.]*|\w[\w.]*)\s+import\s+.+$")
# "from . import foo" / "from .. import foo, bar"  (names ARE module names here)
FROM_DOT_IMPORT_RE = re.compile(r"^from\s+(\.+)\s+import\s+(.+)$")


def _top_level_name(module_name):
    """'foo.bar' -> 'foo'. Strips leading dots from relative imports."""
    return module_name.lstrip(".").split(".")[0]


def _find_local_module(module_name, root):
    """Return Path to module_name.py if it exists locally, else None."""
    top_level = _top_level_name(module_name)
    if not top_level:
        return None
    candidate = root / f"{top_level}.py"
    return candidate if candidate.exists() else None


def inline_module(module_name, root, visited):
    module_file = _find_local_module(module_name, root)
    if module_file is None:
        return None

    resolved = module_file.resolve()
    if resolved in visited:
        return ""  # already inlined elsewhere in the bundle
    visited.add(resolved)

    lines = module_file.read_text(encoding="utf-8").splitlines(True)
    output = [
        "\n# ==================================================\n",
        f"# BEGIN {module_file.name}\n",
        "# ==================================================\n\n",
    ]
    output.extend(_process_lines(lines, root, visited))
    output.extend([
        "\n# ==================================================\n",
        f"# END {module_file.name}\n",
        "# ==================================================\n\n",
    ])
    return "".join(output)


def _process_lines(lines, root, visited):
    """
    Walk a file's lines, replacing local imports with inlined module
    content. Non-local imports and everything else pass through unchanged.
    """
    output = []
    for line in lines:
        stripped = line.strip()

        # "from . import foo, bar" / "from .. import foo" — names are modules
        m = FROM_DOT_IMPORT_RE.match(stripped)
        if m:
            names = [n.strip().split(" as ")[0].strip() for n in m.group(2).split(",")]
            handled, expanded_lines = _try_inline_all(names, root, visited)
            if handled:
                output.extend(expanded_lines)
                continue
            output.append(line)
            continue

        # "from foo import x" / "from foo.bar import x"
        m = FROM_IMPORT_RE.match(stripped)
        if m:
            module_name = m.group(1)
            expanded = inline_module(module_name, root, visited)
            if expanded is not None:
                if expanded:
                    output.append(expanded)
                continue
            output.append(line)
            continue

        # "import foo" / "import foo, bar, baz"
        m = IMPORT_RE.match(stripped)
        if m:
            names = [n.strip().split(" as ")[0].strip() for n in m.group(1).split(",")]
            handled, expanded_lines = _try_inline_all(names, root, visited)
            if handled:
                output.extend(expanded_lines)
                continue
            # Mixed local/non-local on one line: inline the local ones,
            # keep a rewritten import line for the rest.
            remaining = [n for n in names if _find_local_module(n, root) is None]
            local = [n for n in names if _find_local_module(n, root) is not None]
            if local:
                for n in local:
                    expanded = inline_module(n, root, visited)
                    if expanded:
                        output.append(expanded)
                if remaining:
                    indent = line[: len(line) - len(line.lstrip())]
                    output.append(f"{indent}import {', '.join(remaining)}\n")
                continue
            output.append(line)
            continue

        output.append(line)
    return output


def _try_inline_all(names, root, visited):
    """
    If every name in `names` resolves to a local module, inline all of
    them and report handled=True. Otherwise report handled=False so the
    caller keeps the original line untouched.
    """
    if not names or any(_find_local_module(n, root) is None for n in names):
        return False, []
    expanded_lines = []
    for n in names:
        expanded = inline_module(n, root, visited)
        if expanded:
            expanded_lines.append(expanded)
    return True, expanded_lines


def build(main_file="main.py", output_file="build.py"):
    root = Path(main_file).resolve().parent
    visited = set()

    main_path = root / Path(main_file).name
    if not main_path.exists():
        raise FileNotFoundError(main_path)

    lines = main_path.read_text(encoding="utf-8").splitlines(True)
    output = _process_lines(lines, root, visited)

    Path(output_file).write_text("".join(output), encoding="utf-8")
    print(f"Built {output_file}")
    if visited:
        names = ", ".join(sorted(p.name for p in visited))
        print(f"Inlined: {names}")
    else:
        print("No local modules found to inline.")


if __name__ == "__main__":
    build()