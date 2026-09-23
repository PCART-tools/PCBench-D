def get_base_name_for_op(
    base_name_to_sets_of_related_ops: Dict[str, Set[NSNodeTargetType]],
    op: NSNodeTargetType,
) -> Optional[str]:
    for base_name, set_of_related_ops in base_name_to_sets_of_related_ops.items():
        if op in set_of_related_ops:
            return base_name
    return None
