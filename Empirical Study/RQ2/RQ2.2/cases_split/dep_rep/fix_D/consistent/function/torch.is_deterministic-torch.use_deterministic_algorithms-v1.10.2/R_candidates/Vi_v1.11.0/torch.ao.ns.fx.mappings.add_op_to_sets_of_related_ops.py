def add_op_to_sets_of_related_ops(
    base_name_to_sets_of_related_ops: Dict[str, Set[NSNodeTargetType]],
    op: NSNodeTargetType,
    related_op: Optional[NSNodeTargetType],
) -> None:
    if related_op is not None:
        for base_name, set_of_related_ops in base_name_to_sets_of_related_ops.items():
            if related_op in set_of_related_ops:
                set_of_related_ops.add(op)
                return
        # if we got here, related_op was not found
        raise AssertionError(f"{related_op} was not found")
    else:
        counter = 0
        while str(counter) in base_name_to_sets_of_related_ops:
            counter += 1
        base_name_to_sets_of_related_ops[str(counter)] = set([op])
