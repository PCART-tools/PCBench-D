def disable(fn=None, recursive=True):
    """
    This function provides a decorator to disable compilation on a function.
    It also provides the option of recursively disabling called functions.

    Args:
        fn (optional): The function to disable
        recursive (optional): A boolean value indicating whether the disabling should be recursive.
    """
    import torch._dynamo

    return torch._dynamo.disable(fn, recursive)
