def host_memory_stats() -> dict[str, Any]:
    r"""Return a dictionary of CUDA memory allocator statistics for a given device.

     The return value of this function is a dictionary of statistics, each of
     which is a non-negative integer.

     Core statistics:

     - ``"allocated.{current,peak,allocated,freed}"``:
       number of allocation requests received by the memory allocator.
     - ``"allocated_bytes.{current,peak,allocated,freed}"``:
       amount of allocated memory.
     - ``"segment.{current,peak,allocated,freed}"``:
       number of reserved segments from ``cudaMalloc()``.
     - ``"reserved_bytes.{current,peak,allocated,freed}"``:
       amount of reserved memory.

     For these core statistics, values are broken down as follows.

     Metric type:

     - ``current``: current value of this metric.
     - ``peak``: maximum value of this metric.
     - ``allocated``: historical total increase in this metric.
     - ``freed``: historical total decrease in this metric.

     In addition to the core statistics, we also provide some simple event
     counters:

     - ``"num_host_alloc"``: number of CUDA allocation calls. This includes both
       cudaHostAlloc and cudaHostRegister.
     - ``"num_host_free"``: number of CUDA free calls. This includes both cudaHostFree
       and cudaHostUnregister.

     Finally, we also provide some simple timing counters:

     - ``"host_alloc_time.{total,max,min,count,avg}"``:
       timing of allocation requests going through CUDA calls.
     - ``"host_free_time.{total,max,min,count,avg}"``:
       timing of free requests going through CUDA calls.

    For these timing statistics, values are broken down as follows.

     Metric type:

     - ``total``: total time spent.
     - ``max``: maximum value per call.
     - ``min``: minimum value per call.
     - ``count``: number of times it was called.
     - ``avg``: average time per call.
    """
    result = []

    def _recurse_add_to_result(prefix, obj):
        if isinstance(obj, dict):
            if len(prefix) > 0:
                prefix += "."
            for k, v in obj.items():
                _recurse_add_to_result(prefix + k, v)
        else:
            result.append((prefix, obj))

    stats = host_memory_stats_as_nested_dict()
    _recurse_add_to_result("", stats)
    result.sort()

    return collections.OrderedDict(result)
