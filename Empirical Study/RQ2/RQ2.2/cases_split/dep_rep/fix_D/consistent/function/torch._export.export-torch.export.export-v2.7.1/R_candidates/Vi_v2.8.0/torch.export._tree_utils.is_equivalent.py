def is_equivalent(
    spec1: TreeSpec,
    spec2: TreeSpec,
    equivalence_fn: Callable[[Optional[type], Context, Optional[type], Context], bool],
) -> bool:
    """Customizable equivalence check for two TreeSpecs.

    Arguments:
        spec1: The first TreeSpec to compare
        spec2: The second TreeSpec to compare
        equivalence_fn: A function to determine the equivalence of two
            TreeSpecs by examining their types and contexts. It will be called like:

                equivalence_fn(spec1.type, spec1.context, spec2.type, spec2.context)

            This function will be applied recursively to all children.

    Returns:
        True if the two TreeSpecs are equivalent, False otherwise.
    """
    if not equivalence_fn(spec1.type, spec1.context, spec2.type, spec2.context):
        return False

    # Recurse on children
    if len(spec1.children_specs) != len(spec2.children_specs):
        return False

    for child_spec1, child_spec2 in zip(spec1.children_specs, spec2.children_specs):
        if not is_equivalent(child_spec1, child_spec2, equivalence_fn):
            return False

    return True
