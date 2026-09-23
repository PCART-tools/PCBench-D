def wait(future):
    r"""
    Forces completion of a `torch.jit.Future[T]` asynchronous task, returning the
    result of the task. See :func:`~fork` for docs and examples.
    Args:
        func (torch.jit.Future[T]): an asynchronous task reference, created through `torch.jit.fork`
    Returns:
        `T`: the return value of the the completed task
    """
    return torch._C.wait(future)
