def set_stream(stream: torch.Stream) -> None:
    r"""Set the current stream to a given stream.

    Args:
        stream (torch.Stream): a given stream that must match the current :ref:`accelerator<accelerators>` device type.

    .. note:: This function will set the current device index to the device index of the given stream.
    """
    torch._C._accelerator_setStream(stream)
