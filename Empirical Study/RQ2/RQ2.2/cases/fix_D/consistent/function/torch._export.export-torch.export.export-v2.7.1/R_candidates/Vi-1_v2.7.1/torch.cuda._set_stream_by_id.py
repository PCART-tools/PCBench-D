def _set_stream_by_id(stream_id, device_index, device_type):
    r"""set stream specified by the stream id, device index and
        device type

    Args: stream_id (int): stream id in stream pool
          device_index (int): device index in topo
          device_type (int): enum device type
    """
    torch._C._cuda_setStream(
        stream_id=stream_id,
        device_index=device_index,
        device_type=device_type,
    )
