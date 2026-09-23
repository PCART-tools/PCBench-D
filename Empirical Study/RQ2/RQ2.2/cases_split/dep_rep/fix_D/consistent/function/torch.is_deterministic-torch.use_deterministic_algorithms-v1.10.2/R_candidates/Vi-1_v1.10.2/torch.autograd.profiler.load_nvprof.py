def load_nvprof(path):
    """Opens an nvprof trace file and parses autograd annotations.

    Args:
        path (str): path to nvprof trace
    """
    return EventList(parse_nvprof_trace(path))
