@deprecated(
    "torch.utils._pytree._is_leaf is private and will be removed in a future release. "
    "Please use torch.utils._pytree.tree_is_leaf instead.",
    category=FutureWarning,
)
def _is_leaf(tree: PyTree, is_leaf: Optional[Callable[[PyTree], bool]] = None) -> bool:
    return tree_is_leaf(tree, is_leaf=is_leaf)
