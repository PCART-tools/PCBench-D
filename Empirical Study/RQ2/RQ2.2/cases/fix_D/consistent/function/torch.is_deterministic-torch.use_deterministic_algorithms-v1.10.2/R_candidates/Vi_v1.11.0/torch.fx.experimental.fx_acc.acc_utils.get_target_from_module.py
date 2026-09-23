def get_target_from_module(mod: torch.nn.Module, target: str):
    """
    Gets `target` from `mod` and returns it. If `target` is empty then returns `mod.`
    """
    if target == "":
        return mod

    target_atoms = target.split(".")
    curr_obj = mod
    for i, atom in enumerate(target_atoms):
        if not hasattr(curr_obj, atom):
            raise RuntimeError(
                f"Node referenced nonexistent target '{'.'.join(target_atoms[:i])}'; "
                f" original whole target: '{target}'"
            )
        curr_obj = getattr(curr_obj, atom)
    return curr_obj
