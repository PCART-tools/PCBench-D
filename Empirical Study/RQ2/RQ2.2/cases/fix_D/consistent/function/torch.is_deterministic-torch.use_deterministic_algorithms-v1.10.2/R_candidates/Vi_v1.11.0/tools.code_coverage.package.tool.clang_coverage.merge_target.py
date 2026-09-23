def merge_target(raw_file: str, merged_file: str, platform_type: TestPlatform) -> None:
    print_log("start to merge target: ", raw_file)
    # run command
    llvm_tool_path = get_tool_path_by_platform(platform_type)
    subprocess.check_call(
        [
            f"{llvm_tool_path}/llvm-profdata",
            "merge",
            "-sparse",
            raw_file,
            "-o",
            merged_file,
        ]
    )
