def create_subclass_meta(
    curr_args: Union[list[Any], tuple[Any, ...]],
    *,
    count_symints: bool = True,
    with_memory_format: bool = False,
) -> list[Union[PlainTensorMeta, SubclassCreationMeta]]:
    idx = 0
    infos: list[Union[PlainTensorMeta, SubclassCreationMeta]] = []
    for a in curr_args:
        if is_traceable_wrapper_subclass(a):
            assert isinstance(a, Tensor)
            start_idx = idx
            subclass_meta, _ = create_subclass_metadata(
                a,
                start_idx,
                count_symints=count_symints,
                with_memory_format=with_memory_format,
            )
            infos.append(subclass_meta)
            cnt = subclass_meta.arg_count
        else:
            infos.append(
                PlainTensorMeta(
                    idx,
                    memory_format=maybe_suggest_memory_format(a, with_memory_format),
                )
            )
            cnt = 1
        idx += cnt
    return infos
