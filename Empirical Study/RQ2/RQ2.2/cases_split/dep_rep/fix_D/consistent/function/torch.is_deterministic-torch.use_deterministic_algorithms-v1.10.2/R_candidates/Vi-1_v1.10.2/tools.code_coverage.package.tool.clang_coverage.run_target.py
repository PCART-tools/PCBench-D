def run_target(
    binary_file: str, raw_file: str, test_type: TestType, platform_type: TestPlatform
) -> None:
    print_log("start run: ", binary_file)
    # set environment variable -- raw profile output path of the binary run
    os.environ["LLVM_PROFILE_FILE"] = raw_file
    # run binary
    if test_type == TestType.PY and platform_type == TestPlatform.OSS:
        from ..oss.utils import run_oss_python_test

        run_oss_python_test(binary_file)
    else:
        run_cpp_test(binary_file)
