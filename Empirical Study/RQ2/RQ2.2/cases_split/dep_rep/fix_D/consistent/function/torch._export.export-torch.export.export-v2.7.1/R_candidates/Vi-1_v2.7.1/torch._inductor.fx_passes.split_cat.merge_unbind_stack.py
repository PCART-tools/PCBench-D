@register_graph_pattern(
    CallFunction([torch.stack, torch.cat], getitem_unbind, Ignored(), _users=MULTIPLE),
    pass_dict=construct_pattern_matcher_pass("unbind_stack_pass"),
)
@register_graph_pattern(
    CallFunction(
        [torch.stack, torch.cat], getitem_unbind, dim=Ignored(), _users=MULTIPLE
    ),
    pass_dict=construct_pattern_matcher_pass("unbind_stack_pass"),
)
@register_graph_pattern(
    CallFunction(
        [torch.stack, torch.cat], tensors=getitem_unbind, dim=Ignored(), _users=MULTIPLE
    ),
    pass_dict=construct_pattern_matcher_pass("unbind_stack_pass"),
)
def merge_unbind_stack(match: Match, unbind_input: torch.fx.Node, dim: int):
    unbind_node = next(node for node in match.nodes if node.target == torch.unbind)
    UnbindCatRemover().remove_unbind(match.graph, unbind_node)
