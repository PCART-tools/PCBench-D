def allgather_run(cmd):
    proc = subprocess.run(shlex.split(cmd), capture_output=True)
    assert(proc.returncode == 0)
    return allgather_object(proc.stdout.decode("utf-8"))
