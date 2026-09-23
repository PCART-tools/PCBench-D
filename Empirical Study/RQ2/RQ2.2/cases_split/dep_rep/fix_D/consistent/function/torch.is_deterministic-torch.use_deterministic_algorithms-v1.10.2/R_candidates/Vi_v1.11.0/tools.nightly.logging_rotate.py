def logging_rotate() -> None:
    log_base = logging_base_dir()
    old_logs = os.listdir(log_base)
    old_logs.sort(reverse=True)
    for stale_log in old_logs[1000:]:
        # Sanity check that it looks like a log
        if LOG_DIRNAME_RE.fullmatch(stale_log) is not None:
            shutil.rmtree(os.path.join(log_base, stale_log))
