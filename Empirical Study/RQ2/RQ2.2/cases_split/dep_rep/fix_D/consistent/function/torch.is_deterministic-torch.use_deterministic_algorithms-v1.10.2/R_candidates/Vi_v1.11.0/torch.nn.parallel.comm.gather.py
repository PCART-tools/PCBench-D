def gather(tensors, dim=0, destination=None, *, out=None):
    r"""Gathers tensors from multiple GPU devices.

    Args:
        tensors (Iterable[Tensor]): an iterable of tensors to gather.
          Tensor sizes in all dimensions other than :attr:`dim` have to match.
        dim (int, optional): a dimension along which the tensors will be
          concatenated. Default: ``0``.
        destination (torch.device, str, or int, optional): the output device.
          Can be CPU or CUDA. Default: the current CUDA device.
        out (Tensor, optional, keyword-only): the tensor to store gather result.
          Its sizes must match those of :attr:`tensors`, except for :attr:`dim`,
          where the size must equal ``sum(tensor.size(dim) for tensor in tensors)``.
          Can be on CPU or CUDA.

    .. note::
        :attr:`destination` must not be specified when :attr:`out` is specified.

    Returns:
        - If :attr:`destination` is specified,
            a tensor located on :attr:`destination` device, that is a result of
            concatenating :attr:`tensors` along :attr:`dim`.
        - If :attr:`out` is specified,
            the :attr:`out` tensor, now containing results of concatenating
            :attr:`tensors` along :attr:`dim`.
    """
    tensors = [_handle_complex(t) for t in tensors]
    if out is None:
        if destination == -1:
            warnings.warn(
                'Using -1 to represent CPU tensor is deprecated. Please use a '
                'device object or string instead, e.g., "cpu".')
        destination = _get_device_index(destination, allow_cpu=True, optional=True)
        return torch._C._gather(tensors, dim, destination)
    else:
        if destination is not None:
            raise RuntimeError(
                "'destination' must not be specified when 'out' is specified, but "
                "got destination={}".format(destination))
        return torch._C._gather_out(tensors, out, dim)
