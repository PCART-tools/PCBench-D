@register_inference_rule(_assert_is_none)
def assert_inference_rule(n: Node, symbols, constraints, counter):
    assert len(n.users) == 0
    return [], counter
