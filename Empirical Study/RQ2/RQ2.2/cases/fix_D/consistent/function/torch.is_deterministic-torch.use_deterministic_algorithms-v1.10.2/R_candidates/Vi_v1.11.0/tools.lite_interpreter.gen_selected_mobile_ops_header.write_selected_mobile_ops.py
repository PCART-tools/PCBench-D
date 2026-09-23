def write_selected_mobile_ops(
        output_file_path: str,
        selective_builder: SelectiveBuilder,
) -> None:
    root_ops = extract_root_operators(selective_builder)
    custom_classes = selective_builder.custom_classes
    build_features = selective_builder.build_features
    with open(output_file_path, "wb") as out_file:
        body_parts = [selected_mobile_ops_preamble]
        # This condition checks if we are in selective build.
        # if these lists are not defined the corresponding selective build macros trivially return the item in question was selected
        if not selective_builder.include_all_operators:
            body_parts.append("#define TORCH_OPERATOR_WHITELIST " + (";".join(sorted(root_ops))) + ";\n\n")
            # This condition checks if we are in tracing based selective build
            if selective_builder.include_all_non_op_selectives is False:
                body_parts.append("#define TORCH_CUSTOM_CLASS_ALLOWLIST " + (";".join(sorted(custom_classes))) + ";\n\n")
                body_parts.append("#define TORCH_BUILD_FEATURE_ALLOWLIST " + (";".join(sorted(build_features))) + ";\n\n")

        body_parts.append(get_selected_kernel_dtypes_code(selective_builder))
        header_contents = "".join(body_parts)
        out_file.write(header_contents.encode("utf-8"))
