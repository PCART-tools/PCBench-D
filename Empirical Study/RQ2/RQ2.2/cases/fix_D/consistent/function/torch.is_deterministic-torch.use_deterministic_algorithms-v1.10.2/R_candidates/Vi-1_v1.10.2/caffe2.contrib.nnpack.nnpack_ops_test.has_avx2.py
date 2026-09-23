def has_avx2():
    import subprocess
    try:
        subprocess.check_output(["grep", "avx2", "/proc/cpuinfo"])
        return True
    except subprocess.CalledProcessError:
        # grep exits with rc 1 on no matches
        return False
