def combine_selective_builders(lhs: SelectiveBuilder, rhs: SelectiveBuilder) -> SelectiveBuilder:
    include_all_operators = lhs.include_all_operators or rhs.include_all_operators
    debug_info = merge_debug_info(lhs._debug_info, rhs._debug_info)
    operators = merge_operator_dicts(lhs.operators, rhs.operators)
    kernel_metadata = merge_kernel_metadata(lhs.kernel_metadata, rhs.kernel_metadata)
    include_all_kernel_dtypes = lhs.include_all_kernel_dtypes or rhs.include_all_kernel_dtypes
    return SelectiveBuilder(
        include_all_operators,
        debug_info,
        operators,
        kernel_metadata,
        include_all_kernel_dtypes,
    )
