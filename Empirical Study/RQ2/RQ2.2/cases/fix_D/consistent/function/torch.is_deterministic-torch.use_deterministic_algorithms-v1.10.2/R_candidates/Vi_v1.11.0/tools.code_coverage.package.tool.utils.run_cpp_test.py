def run_cpp_test(binary_file: str) -> None:
    # cpp test binary
    try:
        subprocess.check_call(binary_file)
    except subprocess.CalledProcessError:
        print_error(f"Binary failed to run: {binary_file}")
