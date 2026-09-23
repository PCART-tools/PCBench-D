def get_type_promotion_rule(
    diagnostic: diagnostics.Diagnostic,
    node: torch.fx.Node,
    type_promotion_table: TypePromotionTable,
) -> TypePromotionRule | None:
    """Get type promotion rule for a node.

    Args:
        diagnostic: Diagnostic object.
        node: Node to get type promotion rule for.
        type_promotion_table: Type promotion table.

    Returns:
        Type promotion rule for the node. None if no rule is found or if the node is not
        representing a torch operator.
    """
    op = node.target
    if not isinstance(op, torch._ops.OpOverload):
        # TODO(bowbao): diagnostic.emit and diagnostic.set_message api.
        diagnostic.message = (
            f"Skipped for {diagnostics.format_argument(node)}: "
            f"node.target is not OpOverload. Got type: {type(op)}"
        )
        return None
    if (rule := type_promotion_table.get_rule(op.overloadpacket)) is None:
        diagnostic.message = (
            f"Skipped for {diagnostics.format_argument(node)}: "
            f"Cannot find type promotion rule for op: {op}"
        )
        return None

    diagnostic.info("Found type promotion rule: %s", rule)
    return rule
