def run_cmd(cmd: List[str]) -> None:
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
    stdout, stderr = result.stdout.decode("utf-8").strip(), result.stderr.decode("utf-8").strip()
    print(stdout)
    print(stderr)
    if result.returncode != 0:
        print(f"Failed to run {cmd}")
        exit(1)
