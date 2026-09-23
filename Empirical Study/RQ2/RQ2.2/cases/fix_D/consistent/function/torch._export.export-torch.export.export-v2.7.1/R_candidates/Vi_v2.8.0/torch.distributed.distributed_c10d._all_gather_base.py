@_exception_logger
@deprecated(
    "`torch.distributed._all_gather_base` is a private function and will be deprecated. "
    "Please use `torch.distributed.all_gather_into_tensor` instead.",
    category=FutureWarning,
)
def _all_gather_base(output_tensor, input_tensor, group=None, async_op=False):
    """
    Single tensor all gather. Gathers a single tensor from all ranks, and puts them in a single output tensor.

    Args:
        output_tensor (Tensor): Output tensor. It should contain
            correctly-sized tensors to be used for output of the collective.
        input_tensor (Tensor): Tensor to be broadcast from current process.
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        async_op (bool, optional): Whether this op should be an async op

    Returns:
        Async work handle, if async_op is set to True.
        None, if not async_op or if not part of the group

    .. warning::
        `_all_gather_base` is a private function. Users should use
        `all_gather_into_tensor` instead.

    """
    return all_gather_into_tensor(output_tensor, input_tensor, group, async_op)
