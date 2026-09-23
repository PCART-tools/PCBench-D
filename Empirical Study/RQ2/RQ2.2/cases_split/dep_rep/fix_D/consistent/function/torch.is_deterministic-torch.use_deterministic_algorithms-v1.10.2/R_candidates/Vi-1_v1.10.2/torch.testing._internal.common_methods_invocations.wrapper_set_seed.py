def wrapper_set_seed(op, input, *args, **kwargs):
    """Wrapper to set seed manually for some functions like dropout
    See: https://github.com/pytorch/pytorch/pull/62315#issuecomment-896143189 for more details.
    """
    torch.manual_seed(42)
    return op(input, *args, **kwargs)
