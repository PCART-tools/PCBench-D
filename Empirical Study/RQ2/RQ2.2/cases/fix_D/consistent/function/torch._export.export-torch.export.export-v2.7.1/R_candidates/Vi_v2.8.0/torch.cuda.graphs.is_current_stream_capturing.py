def is_current_stream_capturing():
    r"""Return True if CUDA graph capture is underway on the current CUDA stream, False otherwise.

    If a CUDA context does not exist on the current device, returns False without initializing the context.
    """
    return _cuda_isCurrentStreamCapturing()
