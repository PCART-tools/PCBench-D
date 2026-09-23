def export_target(
    merged_file: str,
    json_file: str,
    binary_file: str,
    shared_library_list: List[str],
    platform_type: TestPlatform,
) -> None:
    if binary_file is None:
        raise Exception(f"{merged_file} doesn't have corresponding binary!")
    print_log("start to export: ", merged_file)
    # run export
    cmd_shared_library = (
        ""
        if not shared_library_list
        else f" -object  {' -object '.join(shared_library_list)}"
    )
    # if binary_file = "", then no need to add it (python test)
    cmd_binary = "" if not binary_file else f" -object {binary_file} "
    llvm_tool_path = get_tool_path_by_platform(platform_type)

    cmd = f"{llvm_tool_path}/llvm-cov export {cmd_binary} {cmd_shared_library}  -instr-profile={merged_file} > {json_file}"
    os.system(cmd)
