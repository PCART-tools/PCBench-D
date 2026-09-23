def unwrap_tensor_subclasses(
    wrapped_args: list[Union[Tensor, int]],
    *,
    append_symints: bool,
):
    def flatten_subclass(t: Union[Tensor, int], *, out=None):
        # unwrap a subclass into plain tensors and their size/stride if "append_symint"
        # is True
        if not is_traceable_wrapper_subclass(t):
            out.append(t)
            return

        attrs, _ = t.__tensor_flatten__()

        for attr in attrs:
            inner_tensor = getattr(t, attr)
            flatten_subclass(inner_tensor, out=out)

        if append_symints:
            out.extend(filter_symints(t.size()))
            out.extend(filter_symints(t.stride()))

    xs_inner: list[Union[int, Tensor, SymInt]] = []

    for x in wrapped_args:
        flatten_subclass(typing.cast(Tensor, x), out=xs_inner)

    return xs_inner
