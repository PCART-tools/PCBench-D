def register_dataclass(
    cls: type[Any],
    *,
    serialized_type_name: Optional[str] = None,
) -> None:
    """
    Registers a dataclass as a valid input/output type for :func:`torch.export.export`.

    Args:
        cls: the dataclass type to register
        serialized_type_name: The serialized name for the dataclass. This is
        required if you want to serialize the pytree TreeSpec containing this
        dataclass.

    Example::

        import torch
        from dataclasses import dataclass

        @dataclass
        class InputDataClass:
            feature: torch.Tensor
            bias: int

        @dataclass
        class OutputDataClass:
            res: torch.Tensor

        torch.export.register_dataclass(InputDataClass)
        torch.export.register_dataclass(OutputDataClass)

        class Mod(torch.nn.Module):
            def forward(self, x: InputDataClass) -> OutputDataClass:
                res = x.feature + x.bias
                return OutputDataClass(res=res)

        ep = torch.export.export(Mod(), (InputDataClass(torch.ones(2, 2), 1), ))
        print(ep)

    """

    from torch._export.utils import register_dataclass_as_pytree_node

    return register_dataclass_as_pytree_node(
        cls, serialized_type_name=serialized_type_name
    )
