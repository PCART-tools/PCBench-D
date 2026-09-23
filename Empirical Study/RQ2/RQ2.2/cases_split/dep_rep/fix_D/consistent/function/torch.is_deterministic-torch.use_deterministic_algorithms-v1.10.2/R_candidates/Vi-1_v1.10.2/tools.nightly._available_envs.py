def _available_envs() -> Dict[str, str]:
    cmd = ["conda", "env", "list"]
    p = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    lines = p.stdout.splitlines()
    envs = {}
    for line in map(str.strip, lines):
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) == 1:
            # unnamed env
            continue
        envs[parts[0]] = parts[-1]
    return envs
