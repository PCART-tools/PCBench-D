def run_oss_python_test(binary_file: str) -> None:
    # python test script
    try:
        subprocess.check_call(
            binary_file, shell=True, cwd=get_oss_binary_folder(TestType.PY)
        )
    except subprocess.CalledProcessError:
        print_error(f"Binary failed to run: {binary_file}")
