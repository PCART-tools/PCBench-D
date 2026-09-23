def python_path(cpath):
    for maybe in cpath.split(':'):
        candidate = Path(maybe) / "python"
        if candidate.exists():
            cmd = [str(candidate), '-c', 'import sys; print(":".join(sys.path))']
            return subprocess.check_output(cmd).decode('utf-8').strip('\n').split(':')
    raise RuntimeError('could not find real python')
