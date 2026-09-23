@functools.lru_cache(None)
def has_dot() -> bool:
    try:
        subprocess.check_output(["which", "dot"], stderr=subprocess.PIPE)
        return True
    except subprocess.SubprocessError:
        return False
