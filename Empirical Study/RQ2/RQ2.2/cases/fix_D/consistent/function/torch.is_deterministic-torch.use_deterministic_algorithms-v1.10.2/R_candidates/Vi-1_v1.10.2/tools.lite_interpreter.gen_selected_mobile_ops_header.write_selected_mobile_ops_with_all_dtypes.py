def write_selected_mobile_ops_with_all_dtypes(
    output_file_path: str,
    root_ops: Set[str],
) -> None:
    with open(output_file_path, "wb") as out_file:
        body_parts = [selected_mobile_ops_preamble]
        body_parts.append("#define TORCH_OPERATOR_WHITELIST " + (";".join(sorted(root_ops))) + ";\n\n")

        selective_builder = SelectiveBuilder.get_nop_selector()
        body_parts.append(get_selected_kernel_dtypes_code(selective_builder))

        header_contents = "".join(body_parts)
        out_file.write(header_contents.encode("utf-8"))
