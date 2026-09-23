def get_numel_argdefs(kernel):
    numel_argdefs = [
        f"{tree.prefix}numel"
        for tree in kernel.range_trees
        if not tree.is_reduction or kernel.inside_reduction
    ]

    return numel_argdefs
