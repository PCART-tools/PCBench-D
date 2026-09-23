def test(cmd, limit):
    print(f"Testing PYTORCH_JIT_OPT_LIMIT=tensorexpr_fuser={limit} {cmd}")
    p = subprocess.run(
        f"PYTORCH_JIT_OPT_LIMIT=tensorexpr_fuser={limit} {cmd}",
        shell=True,
        capture_output=True,
        encoding="utf-8",
        check=False,
    )
    print(p.stdout)
    f = "INTERNAL ASSERT FAILED"
    if f in p.stdout or f in p.stderr:
        print("skip")
        return -1
    if p.returncode == 0:
        print("good")
        return 1
    print("bad")
    return 0
