def run_command(
    args: List[str],
    *,
    retries: int,
    timeout: int,
) -> "subprocess.CompletedProcess[bytes]":
    remaining_retries = retries
    while True:
        try:
            return _run_command(args, timeout=timeout)
        except subprocess.TimeoutExpired as err:
            if remaining_retries == 0:
                raise err
            remaining_retries -= 1
            logging.warning(
                "(%s/%s) Retrying because command failed with: %r",
                retries - remaining_retries,
                retries,
                err,
            )
            time.sleep(1)
