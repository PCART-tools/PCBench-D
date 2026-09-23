def record_stream(tensor: torch.Tensor, stream: AbstractStream) -> None:
    """:meth:`torch.Tensor.record_stream` for either CPU or CUDA stream."""
    if is_cuda(stream):
        # NOTE(sublee): record_stream() on a shifted view tensor throws
        # RuntimeError in PyTorch 1.1.0, and does nothing in 1.2.0. To safely
        # protect the tensor against unexpected reallocation, here we use a
        # temporal tensor associated with the same storage without shifting as
        # a workaround.
        #
        # Issue: https://github.com/pytorch/pytorch/issues/27366
        #
        tensor = tensor.new_empty([0]).set_(tensor.storage())

        # Typechecking: torch.cuda.Stream is incompatible with torch._C.Stream
        tensor.record_stream(as_cuda(stream))  # type: ignore[arg-type]
