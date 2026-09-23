def gen_compile_commands() -> None:
    os.environ["USE_NCCL"] = "0"
    os.environ["USE_DEPLOY"] = "1"
    os.environ["CC"] = "clang"
    os.environ["CXX"] = "clang++"
    run_timed_cmd([sys.executable, "setup.py", "--cmake-only", "build"])
