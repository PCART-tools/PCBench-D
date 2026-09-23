def register_dataclass(cls: type[Any]) -> None:
    """Registers a ``dataclasses.dataclass`` type as a pytree node.

    This is a simpler API than :func:`register_pytree_node` for registering
    a dataclass.

    Args:
        cls: the dataclass type to register

    Example:

        >>> from torch import Tensor
        >>> from dataclasses import dataclass
        >>> import torch.utils._pytree as pytree
        >>>
        >>> @dataclass
        >>> class Point:
        >>>     x: Tensor
        >>>     y: Tensor
        >>>
        >>> pytree.register_dataclass(Point)
        >>>
        >>> point = Point(torch.tensor(0), torch.tensor(1))
        >>> point = pytree.tree_map(lambda x: x + 1, point)
        >>> assert torch.allclose(point.x, torch.tensor(1))
        >>> assert torch.allclose(point.y, torch.tensor(2))

    """
    import torch.export

    # Eventually we should move the export code here. It is not specific to export,
    # aside from the serialization pieces.
    torch.export.register_dataclass(cls)
