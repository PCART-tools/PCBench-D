@contextlib.contextmanager
def jvp_increment_nesting():
    try:
        yield enter_jvp_nesting()
    finally:
        exit_jvp_nesting()
