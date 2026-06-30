# Simple binary min-heap for VEX V5 (subset of heapq)

def heappush(heap, item):
    """
    Push item into heap.
    heap: list
    item: comparable tuple like (f_score, node)
    """
    heap.append(item)
    _heapvex_sift_up(heap, len(heap) - 1)
 

def heappop(heap):
    """
    Pop smallest item from heap.
    """
    if not heap:
        return []
 
    _heapvex_swap(heap, 0, len(heap) - 1)
    item = heap.pop()
 
    if heap:
        _heapvex_sift_down(heap, 0)
 
    return item
 
# ------------------------------------------------------
# Internal helpers
# ------------------------------------------------------
 
def _heapvex_sift_up(heap, i):
    while i > 0:
        parent = (i - 1) // 2
 
        if heap[i][0] < heap[parent][0]:
            _heapvex_swap(heap, i, parent)
            i = parent
        else:
            break
 
 
def _heapvex_sift_down(heap, i):
    n = len(heap)
 
    while True:
        left = 2 * i + 1
        right = 2 * i + 2
        smallest = i
 
        if left < n and heap[left][0] < heap[smallest][0]:
            smallest = left
 
        if right < n and heap[right][0] < heap[smallest][0]:
            smallest = right
 
        if smallest != i:
            _heapvex_swap(heap, i, smallest)
            i = smallest
        else:
            break
 
 
def _heapvex_swap(heap, i, j):
    tmp = heap[i]
    heap[i] = heap[j]
    heap[j] = tmp