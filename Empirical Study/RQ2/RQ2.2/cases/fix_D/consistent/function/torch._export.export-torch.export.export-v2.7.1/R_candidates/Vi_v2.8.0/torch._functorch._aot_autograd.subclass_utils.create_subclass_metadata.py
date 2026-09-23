def create_subclass_metadata(
    a: Any, start_idx: int, count_symints: bool, with_memory_format: bool = False
):
    if not is_traceable_wrapper_subclass(a):
        idx = start_idx + 1
        return (
            PlainTensorMeta(
                idx,
                memory_format=maybe_suggest_memory_format(a, with_memory_format),
            ),
            idx,
        )

    inner_keys, metadata = a.__tensor_flatten__()
    new_start_idx = start_idx
    attrs = {}

    for key in inner_keys:
        new_subclass_meta, new_start_idx = create_subclass_metadata(
            getattr(a, key),
            new_start_idx,
            count_symints=count_symints,
            with_memory_format=with_memory_format,
        )
        attrs[key] = new_subclass_meta

    # It *must* be because is_traceable_wrapper_subclass() - but mypy is not smart.
    assert isinstance(a, Tensor)

    new_start_idx = (
        new_start_idx
        + count_symints * len(filter_symints(a.size()))
        + count_symints * len(filter_symints(a.stride()))
    )

    return (
        SubclassCreationMeta(
            flat_tensor_start_idx=start_idx,
            arg_count=new_start_idx - start_idx,
            included_subclass_symints=count_symints,
            attrs=attrs,
            meta=metadata,
            outer_size=a.size(),  # type: ignore[attr-defined, arg-type]
            outer_stride=a.stride(),  # type: ignore[arg-type]
            original_subclass=a,
            memory_format=maybe_suggest_memory_format(a, with_memory_format),
        ),
        new_start_idx,
    )
