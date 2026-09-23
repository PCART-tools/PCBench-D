def ncu_analyzer(
    benchmark_name: str, benchmark_compiled_module_fn: BenchmarkCallableType
) -> None:
    import inspect
    import os
    import subprocess

    module_file = inspect.getfile(benchmark_compiled_module_fn)
    module_dir = os.path.dirname(module_file)
    module_name = os.path.splitext(os.path.basename(module_file))[0]

    ncu_dir = tempfile.gettempdir()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    ncu_output = os.path.join(ncu_dir, f"ncu_output_{timestamp}.ncu-rep")
    python_cmd = (
        f"""import sys; sys.path.insert(0, '{module_dir}'); """
        f"""from {module_name} import benchmark_compiled_module; """
        """benchmark_compiled_module(times=1, repeat=1)"""
    )

    ncu_cmd = [
        "ncu",
        "--target-processes",
        "all",
        "--replay-mode",
        "kernel",
        "--kernel-name-base",
        "function",
        "--print-units",
        "base",
        "--set",
        "full",
        "--import-source",
        "yes",
        "--force-overwrite",
        "--export",
        ncu_output,
        "python",
        "-c",
        python_cmd,
    ]

    try:
        subprocess.run(ncu_cmd, check=True)
        print(f"\nNCU profiling results for benchmark {benchmark_name}:")
        print(f"NCU report has been written to {ncu_output}")

    except subprocess.CalledProcessError as e:
        print(f"NCU profiling failed with error: {e}")
        return
