def pid_exists(pid):
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False
