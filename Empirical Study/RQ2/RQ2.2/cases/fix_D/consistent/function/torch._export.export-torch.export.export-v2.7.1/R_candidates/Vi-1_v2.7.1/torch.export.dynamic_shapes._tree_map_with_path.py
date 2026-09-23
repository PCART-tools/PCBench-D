def _tree_map_with_path(
    func: Callable[..., Any],
    tree: Any,
    *dynamic_shapes: Any,
    tree_name: Optional[str] = None,
) -> Any:
    """
    Customized tree_map for mapping pytrees to dynamic_shapes.

    For built-in types (e.g., standard collections) this behaves exactly like tree_map.

    OTOH for a user-defined class C registered with pytree, we cannot assume that a C
    containing tensors can be mapped to a C containing dynamic shapes (i.e., C may not
    be a polymorphic container). In that case we use the flattened form of C instead.
    Thus a C(**tensors) that flattens to (**tensors) will map to (**dynamic_shapes).

    Args:
        func: function to apply to each (int, float, str, bool, None, torch.Tensor)
        tree: input pytree
        dynamic_shapes: zero or more (typically one) dynamic_shapes to match

    Returns:
        output pytree mapping func to each (int, float, str, bool, None, torch.Tensor)
    """

    def is_leaf(t):
        # BUILTIN_TYPES is a subset of SUPPORTED_NODES, the latter being all types
        # registered with pytree. Types *not* in BUILTIN_TYPES include primitive types
        # (int, float, str, bool, None, torch.Tensor), which are not in SUPPORTED_NODES,
        # as well as user-defined classes registered with pytree, which are.
        return _get_node_type(t) not in BUILTIN_TYPES

    def f(path, t, *dynamic_shapes):
        typ = _get_node_type(t)
        # typ is not in BUILTIN_TYPES
        if typ in SUPPORTED_NODES:
            # thus typ is a user-defined class registered with pytree,
            # in which case flatten and recurse
            return tree_map_with_path(
                f,
                SUPPORTED_NODES[typ].flatten_fn(t)[0],
                *dynamic_shapes,
                is_leaf=is_leaf,
            )
        else:
            return func(path, t, *dynamic_shapes)

    try:
        return tree_map_with_path(f, tree, *dynamic_shapes, is_leaf=is_leaf)
    except ValueError as e:
        if "mismatch" in e.args[0]:
            # When PyTree finds a structural mismatch between tree and dynamic_shapes,
            # the error message is unfortunately quite horrible. Let's fix that.
            assert dynamic_shapes, "Cannot be a mismatch if there is no dynamic_shapes"
            assert tree_name, "Must provide a tree_name when there might be a mismatch"

            def _key(type_, context, i):
                # derive a PyTree key given the type, context, and child # of a TreeSpec
                if type_ is dict:
                    return MappingKey(context[i])
                if type_ in (list, tuple):
                    assert context is None
                    return SequenceKey(i)
                raise AssertionError(f"Did not expect type {type_}")

            def raise_mismatch_error(msg):
                from torch._dynamo.exc import UserError, UserErrorType

                raise UserError(
                    UserErrorType.INVALID_INPUT,
                    f"Detected mismatch between the structure of `{tree_name}` and `dynamic_shapes`: {msg}",
                    case_name="dynamic_shapes_validation",
                )

            def _compare(tree, dynamic_shapes, path):
                # raise an error at the point where tree and dynamic_shapes differ,
                # including the path to that point and the reason for the difference
                rendered_path = keystr(path)
                if isinstance(tree, LeafSpec):
                    return
                if isinstance(dynamic_shapes, LeafSpec):
                    raise_mismatch_error(
                        f"`{tree_name}{rendered_path}` is a {tree.type}, "
                        f"but `dynamic_shapes{rendered_path}` is not"
                    )
                if tree.type != dynamic_shapes.type:
                    raise_mismatch_error(
                        f"`{tree_name}{rendered_path}` is a {tree.type}, "
                        f"but `dynamic_shapes{rendered_path}` is a {dynamic_shapes.type}"
                    )
                if len(tree.children_specs) != len(dynamic_shapes.children_specs):
                    raise_mismatch_error(
                        f"`{tree_name}{rendered_path}` has {len(tree.children_specs)} elements, "
                        f"but `dynamic_shapes{rendered_path}` has {len(dynamic_shapes.children_specs)} elements"
                    )
                if tree.type is dict:
                    # context, children could be out of order
                    if sorted(tree.context) != sorted(dynamic_shapes.context):
                        raise_mismatch_error(
                            f"`{tree_name}{rendered_path}` has keys {tree.context}, "
                            f"but `dynamic_shapes{rendered_path}` has keys {dynamic_shapes.context}"
                        )
                    _remap = dict(
                        zip(dynamic_shapes.context, dynamic_shapes.children_specs)
                    )
                    dynamic_shapes_children_specs = [_remap[k] for k in tree.context]
                else:
                    dynamic_shapes_children_specs = dynamic_shapes.children_specs
                for i, (tree_, dynamic_shapes_) in enumerate(
                    zip(tree.children_specs, dynamic_shapes_children_specs)
                ):
                    _compare(
                        tree_,
                        dynamic_shapes_,
                        path + [_key(tree.type, tree.context, i)],
                    )

            _, tree_spec = tree_flatten(tree, is_leaf=is_leaf)
            for other_tree in dynamic_shapes:
                _, other_tree_spec = tree_flatten(other_tree, is_leaf)
                _compare(tree_spec, other_tree_spec, [])
        raise
