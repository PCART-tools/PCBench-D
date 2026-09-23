def _run_command(
    args: List[str],
    *,
    extra_env: Optional[Dict[str, str]],
) -> "subprocess.CompletedProcess[str]":
    logging.debug(
        "$ %s",
        " ".join(
            ([f"{k}={v}" for (k, v) in extra_env.items()] if extra_env else []) + args
        ),
    )
    start_time = time.monotonic()
    try:
        return subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            encoding="utf-8",
        )
    finally:
        end_time = time.monotonic()
        logging.debug("took %dms", (end_time - start_time) * 1000)
