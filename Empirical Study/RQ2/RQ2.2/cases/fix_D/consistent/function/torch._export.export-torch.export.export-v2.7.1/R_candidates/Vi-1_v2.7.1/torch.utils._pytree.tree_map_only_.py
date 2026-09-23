def tree_map_only_(
    type_or_types_or_pred: Union[TypeAny, Callable[[Any], bool]],
    /,
    func: FnAny[Any],
    tree: PyTree,
    is_leaf: Optional[Callable[[PyTree], bool]] = None,
) -> PyTree:
    return tree_map_(map_only(type_or_types_or_pred)(func), tree, is_leaf=is_leaf)
