def _open_top_level_sequence_if_single_element(
    spec: pytree.TreeSpec,
) -> pytree.TreeSpec:
    if spec.type in (tuple, list) and spec.num_children == 1:
        return spec.children_specs[0]
    return spec
