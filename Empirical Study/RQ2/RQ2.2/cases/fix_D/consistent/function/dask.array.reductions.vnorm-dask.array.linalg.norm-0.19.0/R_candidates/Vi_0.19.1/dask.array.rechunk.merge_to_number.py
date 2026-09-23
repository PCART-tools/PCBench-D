def merge_to_number(desired_chunks, max_number):
    """ Minimally merge the given chunks so as to drop the number of
    chunks below *max_number*, while minimizing the largest width.
    """
    if len(desired_chunks) <= max_number:
        return desired_chunks

    distinct = set(desired_chunks)
    if len(distinct) == 1:
        # Fast path for homogeneous target, also ensuring a regular result
        w = distinct.pop()
        n = len(desired_chunks)
        total = n * w

        desired_width = total // max_number
        width = w * (desired_width // w)
        adjust = (total - max_number * width) // w

        return (width + w,) * adjust + (width,) * (max_number - adjust)

    desired_width = sum(desired_chunks) // max_number
    nmerges = len(desired_chunks) - max_number

    heap = [(desired_chunks[i] + desired_chunks[i + 1], i, i + 1)
            for i in range(len(desired_chunks) - 1)]
    heapq.heapify(heap)

    chunks = list(desired_chunks)

    while nmerges > 0:
        # Find smallest interval to merge
        width, i, j = heapq.heappop(heap)
        # If interval was made invalid by another merge, recompute
        # it, re-insert it and retry.
        if chunks[j] == 0:
            j += 1
            while chunks[j] == 0:
                j += 1
            heapq.heappush(heap, (chunks[i] + chunks[j], i, j))
            continue
        elif chunks[i] + chunks[j] != width:
            heapq.heappush(heap, (chunks[i] + chunks[j], i, j))
            continue
        # Merge
        assert chunks[i] != 0
        chunks[i] = 0   # mark deleted
        chunks[j] = width
        nmerges -= 1

    return tuple(filter(None, chunks))
