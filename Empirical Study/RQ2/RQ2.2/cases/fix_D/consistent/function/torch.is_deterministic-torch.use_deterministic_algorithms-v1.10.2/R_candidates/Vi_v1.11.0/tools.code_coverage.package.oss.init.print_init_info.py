def print_init_info() -> None:
    print_log("pytorch folder: ", get_pytorch_folder())
    print_log("cpp test binaries folder: ", get_oss_binary_folder(TestType.CPP))
    print_log("python test scripts folder: ", get_oss_binary_folder(TestType.PY))
    print_log("compiler type: ", cast(CompilerType, detect_compiler_type()).value)
    print_log(
        "llvm tool folder (only for clang, if you are using gcov please ignore it): ",
        get_llvm_tool_path(),
    )
