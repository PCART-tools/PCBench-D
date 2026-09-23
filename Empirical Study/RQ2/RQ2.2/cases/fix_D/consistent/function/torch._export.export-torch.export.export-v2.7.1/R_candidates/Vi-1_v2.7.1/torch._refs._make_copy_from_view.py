def _make_copy_from_view(fn):
    """
    Given a view function (e.g. torch.diagonal) generates its copy variant (e.g. torch.diagonal_copy)
    """
    aten_fn = getattr(aten, fn.__name__)
    annotations = getattr(fn, "__annotations__", {})
    fn = out_wrapper()(aten_fn)

    @wraps(fn)
    def _fn(*args, out=None, **kwargs):
        result = fn(*args, out=out, **kwargs)
        if out is not None:
            return result

        return pytree.tree_map(
            lambda x: x.clone(memory_format=torch.contiguous_format),
            result,
        )

    copy_name = f"{fn.__name__}_copy"
    _fn.__name__ = copy_name
    _fn.__annotations__.update(annotations)
    register_decomposition(getattr(aten, copy_name))(_fn)
    return _fn
