def get_executable_command(options, allow_pytest, disable_coverage=False):
    if options.coverage and not disable_coverage:
        executable = ["coverage", "run", "--parallel-mode", "--source=torch"]
    else:
        executable = [sys.executable]
    if options.pytest:
        if allow_pytest:
            executable += ["-m", "pytest"]
        else:
            print_to_stderr(
                "Pytest cannot be used for this test. Falling back to unittest."
            )
    return executable
