def gather_paths(env_vars: Iterable[str]) -> List[str]:
    return list(chain(*(os.getenv(v, '').split(os.pathsep) for v in env_vars)))
