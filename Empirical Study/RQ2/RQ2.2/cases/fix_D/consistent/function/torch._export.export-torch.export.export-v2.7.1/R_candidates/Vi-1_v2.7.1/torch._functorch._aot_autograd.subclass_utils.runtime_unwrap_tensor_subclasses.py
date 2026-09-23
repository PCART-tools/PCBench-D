def runtime_unwrap_tensor_subclasses(
    wrapped_args: list[Union[Tensor, int]],
    *,
    append_symints: bool,
    subclass_metas: Optional[list[Union[PlainTensorMeta, SubclassCreationMeta]]] = None,
):
    def flatten_subclass(x: Tensor, meta: Optional[SubclassCreationMeta], *, out):
        if not is_traceable_wrapper_subclass(x):
            out.append(x)
            return out

        assert isinstance(x, Tensor)

        attrs, _ = x.__tensor_flatten__()

        for attr in attrs:
            inner_tensor = getattr(x, attr)
            inner_meta = meta.attrs.get(attr)
            flatten_subclass(inner_tensor, inner_meta, out=out)

        if append_symints:
            assert isinstance(meta, SubclassCreationMeta)
            # outer_size
            size = x.size()
            symint_placeholders = compute_symint_placeholders(meta.outer_size)
            assert len(size) == len(symint_placeholders)
            out.extend(
                [r for (r, is_symint) in zip(size, symint_placeholders) if is_symint]
            )

            # outer_stride
            stride = x.stride()
            symint_placeholders = compute_symint_placeholders(meta.outer_stride)
            assert len(stride) == len(symint_placeholders)
            out.extend(
                [r for (r, is_symint) in zip(stride, symint_placeholders) if is_symint]
            )
        return out

    xs_inner: list[Union[int, Tensor, SymInt]] = []

    if append_symints:
        assert subclass_metas is not None

    for idx, x in enumerate(wrapped_args):
        if not is_traceable_wrapper_subclass(x):
            xs_inner.append(x)
            continue

        if subclass_metas is None:
            get_plain_tensors(typing.cast(Tensor, x), out=xs_inner)
        else:
            meta = subclass_metas[idx]
            assert isinstance(meta, SubclassCreationMeta)
            flatten_subclass(typing.cast(Tensor, x), meta, out=xs_inner)

    return xs_inner
