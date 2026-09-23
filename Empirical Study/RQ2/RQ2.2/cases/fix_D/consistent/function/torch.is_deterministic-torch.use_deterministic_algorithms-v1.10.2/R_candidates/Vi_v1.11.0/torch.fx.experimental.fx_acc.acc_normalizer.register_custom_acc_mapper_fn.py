def register_custom_acc_mapper_fn(
    op_and_target: Tuple[str, Union[str, Callable]],
    arg_replacement_tuples: List[
        Union[
            Tuple[Union[str, Tuple[str, ...]], str],
            Tuple[Union[str, Tuple[str, ...]], str, bool],
        ]
    ],
    needs_shapes_for_normalization=False,
    allow_normalize_from_torch_package=False,
):
    def insert(custom_mapping_fn: Callable):
        _insert_fun(
            op_and_target=op_and_target,
            custom_mapping_fn=custom_mapping_fn,
            arg_replacement_tuples=arg_replacement_tuples,  # type: ignore[arg-type]
            needs_shapes_for_normalization=needs_shapes_for_normalization,
            allow_normalize_from_torch_package=allow_normalize_from_torch_package,
        )
        return custom_mapping_fn

    return insert
