@register_lowering(torch.ops.prims._sink_tokens.default)
def _sink_tokens(tokens):
    return None
