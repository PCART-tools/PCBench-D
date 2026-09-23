@functools.lru_cache()
def logging_record_argv() -> None:
    s = subprocess.list2cmdline(sys.argv)
    with open(os.path.join(logging_run_dir(), "argv"), "w") as f:
        f.write(s)
