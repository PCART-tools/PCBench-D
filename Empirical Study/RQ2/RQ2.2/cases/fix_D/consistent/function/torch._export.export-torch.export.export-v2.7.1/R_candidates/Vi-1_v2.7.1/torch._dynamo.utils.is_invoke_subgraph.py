def is_invoke_subgraph(obj):
    from torch._higher_order_ops.invoke_subgraph import invoke_subgraph_placeholder

    return obj is invoke_subgraph_placeholder
