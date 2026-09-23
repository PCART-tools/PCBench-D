def get_python_run_only(args_run_only: Optional[List[str]]) -> List[str]:
    # if user specifies run-only option
    if args_run_only:
        return args_run_only

    # if not specified, use default setting, different for gcc and clang
    if detect_compiler_type() == CompilerType.GCC:
        return ["run_test.py"]
    else:
        # for clang, some tests will result in too large intermidiate files that can't be merged by llvm, we need to skip them
        run_only: List[str] = []
        binary_folder = get_oss_binary_folder(TestType.PY)
        g = os.walk(binary_folder)
        for _, _, file_list in g:
            for file_name in file_list:
                if file_name in BLOCKED_PYTHON_TESTS or not file_name.endswith(".py"):
                    continue
                run_only.append(file_name)
            # only run tests in the first-level folder in test/
            break
        return run_only
