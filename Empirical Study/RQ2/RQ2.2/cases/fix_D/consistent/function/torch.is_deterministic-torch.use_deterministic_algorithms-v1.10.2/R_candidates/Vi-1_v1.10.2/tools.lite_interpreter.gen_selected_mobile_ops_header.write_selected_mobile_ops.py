def write_selected_mobile_ops(
        output_file_path: str,
        selective_builder: SelectiveBuilder,
) -> None:
    root_ops = extract_root_operators(selective_builder)
    with open(output_file_path, "wb") as out_file:
        body_parts = [selected_mobile_ops_preamble]
        if not selective_builder.include_all_operators:
            body_parts.append("#define TORCH_OPERATOR_WHITELIST " + (";".join(sorted(root_ops))) + ";\n\n")

        body_parts.append(get_selected_kernel_dtypes_code(selective_builder))
        header_contents = "".join(body_parts)
        out_file.write(header_contents.encode("utf-8"))
