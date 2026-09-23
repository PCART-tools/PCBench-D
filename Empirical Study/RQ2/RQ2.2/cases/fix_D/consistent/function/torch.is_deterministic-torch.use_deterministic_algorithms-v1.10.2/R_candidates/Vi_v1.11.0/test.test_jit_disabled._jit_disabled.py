@contextlib.contextmanager
def _jit_disabled():
    cur_env = os.environ.get("PYTORCH_JIT", "1")
    os.environ["PYTORCH_JIT"] = "0"
    try:
        yield
    finally:
        os.environ["PYTORCH_JIT"] = cur_env
