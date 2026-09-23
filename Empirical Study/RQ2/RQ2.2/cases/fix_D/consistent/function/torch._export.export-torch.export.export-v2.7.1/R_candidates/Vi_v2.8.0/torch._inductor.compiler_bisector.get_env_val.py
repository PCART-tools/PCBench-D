@functools.cache
def get_env_val(env_str: str) -> Optional[str]:
    return os.environ.get(env_str, None)
