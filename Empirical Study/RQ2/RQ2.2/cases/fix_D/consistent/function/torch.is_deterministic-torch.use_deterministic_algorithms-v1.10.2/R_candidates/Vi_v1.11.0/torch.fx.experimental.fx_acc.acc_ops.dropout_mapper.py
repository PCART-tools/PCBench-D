@register_custom_acc_mapper_fn(
    op_and_target=("call_function", nn.functional.dropout),
    arg_replacement_tuples=[("input", "input")],
)
@register_custom_acc_mapper_fn(
    op_and_target=("call_method", "detach"), arg_replacement_tuples=[("input", "input")]
)
def dropout_mapper(node: torch.fx.Node, mod: nn.Module):
    """
    Remove dropout node and directly map its input to output.
    """
    return node.kwargs["input"]
