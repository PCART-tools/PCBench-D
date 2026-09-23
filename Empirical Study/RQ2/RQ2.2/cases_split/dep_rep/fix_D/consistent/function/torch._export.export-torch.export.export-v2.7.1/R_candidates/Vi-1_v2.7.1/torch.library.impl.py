@functools.singledispatch
def impl(
    qualname: str,
    types: Union[str, Sequence[str]],
    func: Optional[Callable[_P, _T]] = None,
    *,
    lib: Optional[Library] = None,
) -> object:
    """Register an implementation for a device type for this operator.

    You may pass "default" for ``types`` to register this implementation as the
    default implementation for ALL device types.
    Please only use this if the implementation truly supports all device types;
    for example, this is true if it is a composition of built-in PyTorch operators.

    This API may be used as a decorator. You can use nested decorators
    with this API provided they return a function and are placed inside
    this API (see Example 2).

    Some valid types are: "cpu", "cuda", "xla", "mps", "ipu", "xpu".

    Args:
        qualname (str): Should be a string that looks like "namespace::operator_name".
        types (str | Sequence[str]): The device types to register an impl to.
        lib (Optional[Library]): If provided, the lifetime of this registration
            will be tied to the lifetime of the Library object.

    Examples:
        >>> import torch
        >>> import numpy as np
        >>> # Example 1: Register function.
        >>> # Define the operator
        >>> torch.library.define("mylib::mysin", "(Tensor x) -> Tensor")
        >>>
        >>> # Add implementations for the cpu device
        >>> @torch.library.impl("mylib::mysin", "cpu")
        >>> def f(x):
        >>>     return torch.from_numpy(np.sin(x.numpy()))
        >>>
        >>> x = torch.randn(3)
        >>> y = torch.ops.mylib.mysin(x)
        >>> assert torch.allclose(y, x.sin())
        >>>
        >>> # Example 2: Register function with decorator.
        >>> def custom_decorator(func):
        >>>     def wrapper(*args, **kwargs):
        >>>         return func(*args, **kwargs) + 1
        >>>     return wrapper
        >>>
        >>> # Define the operator
        >>> torch.library.define("mylib::sin_plus_one", "(Tensor x) -> Tensor")
        >>>
        >>> # Add implementations for the operator
        >>> @torch.library.impl("mylib::sin_plus_one", "cpu")
        >>> @custom_decorator
        >>> def f(x):
        >>>     return torch.from_numpy(np.sin(x.numpy()))
        >>>
        >>> # Call the new operator from torch.ops.
        >>> x = torch.randn(3)
        >>>
        >>> y1 = torch.ops.mylib.sin_plus_one(x)
        >>> y2 = torch.sin(x) + 1
        >>> assert torch.allclose(y1, y2)
    """
    return _impl(qualname, types, func, lib=lib, disable_dynamo=False)
