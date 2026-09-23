def run_autogen() -> None:
    run_timed_cmd(
        [
            sys.executable,
            "-m",
            "tools.codegen.gen",
            "-s",
            "aten/src/ATen",
            "-d",
            "build/aten/src/ATen",
            "--per-operator-headers",
        ]
    )

    run_timed_cmd(
        [
            sys.executable,
            "tools/setup_helpers/generate_code.py",
            "--native-functions-path",
            "aten/src/ATen/native/native_functions.yaml",
            "--nn-path",
            "aten/src",
        ]
    )
