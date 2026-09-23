def get_selected_kernel_dtypes_code(
        selective_builder: SelectiveBuilder,
) -> str:
    # See https://www.internalfb.com/intern/paste/P153411698/ for an example of the
    # generated code in case all kernel dtypes are selected and in case some kernel
    # dtypes are selected (i.e. both cases).
    #
    body = "return true;"
    if selective_builder.include_all_operators is False and selective_builder.include_all_non_op_selectives is False:
        body_parts = []
        for kernel_tag, dtypes in selective_builder.kernel_metadata.items():
            conditions = list(map(lambda x: 'scalar_type == at::ScalarType::' + x, dtypes))
            body_parts.append(
                if_condition_template.substitute(
                    kernel_tag_name=kernel_tag,
                    dtype_checks=" || ".join(conditions),
                ),
            )
        body = " else ".join(body_parts)

    header_contents = selected_kernel_dtypes_h_template.substitute(body=body)
    return header_contents
