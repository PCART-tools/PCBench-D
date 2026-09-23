def is_forward_derivative_definition(all_arg_names: List[str], names: Tuple[str, ...]) -> bool:
    if len(names) > 1:
        # Forward definition are always for a single output at a time
        return False
    name = names[0]
    if name not in all_arg_names:
        return True
    else:
        return False
