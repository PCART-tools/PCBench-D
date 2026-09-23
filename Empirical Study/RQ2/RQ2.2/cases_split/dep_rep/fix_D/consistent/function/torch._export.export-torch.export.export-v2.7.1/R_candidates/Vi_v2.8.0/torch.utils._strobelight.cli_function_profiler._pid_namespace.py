def _pid_namespace(pid: Optional[int] = None) -> int:
    """Returns the process's namespace id"""
    pid = pid or os.getpid()
    link = _pid_namespace_link(pid)
    return int(link[link.find("[") + 1 : -1])
