@register_lowering(torch.ops.higher_order.invoke_subgraph, type_promotion_kind=None)
def invoke_subgraph(subgraph_fn: ir.Subgraph, identifier: str, *operands):
    result = ir.InvokeSubgraph.create(subgraph_fn, *operands)
    return list(map(TensorBox.create, result))
