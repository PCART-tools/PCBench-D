def build_invoke_subgraph_variable(**options):
    from .variables.higher_order_ops import TorchHigherOrderOperatorVariable

    return TorchHigherOrderOperatorVariable.make(
        torch._higher_order_ops.invoke_subgraph,
        **options,
    )
