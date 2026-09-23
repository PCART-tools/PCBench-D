@register_inference_rule(torch.nn.modules.sparse.Embedding)
def embedding_inference_rule(n: Node, module_instance, symbols, constraints, counter):
    """
    The output shape differs from the input shape in the last dimension
    """
    assert isinstance(n.args[0], Node)
    return gen_embedding_rules(n, symbols, module_instance.embedding_dim, counter)
