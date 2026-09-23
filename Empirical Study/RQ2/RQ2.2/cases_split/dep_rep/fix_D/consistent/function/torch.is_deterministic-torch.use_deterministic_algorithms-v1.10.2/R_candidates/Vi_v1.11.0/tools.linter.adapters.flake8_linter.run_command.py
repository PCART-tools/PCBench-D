def run_command(
    args: List[str],
    *,
    extra_env: Optional[Dict[str, str]],
    retries: int,
) -> "subprocess.CompletedProcess[str]":
    remaining_retries = retries
    while True:
        try:
            return _run_command(args, extra_env=extra_env)
        except subprocess.CalledProcessError as err:
            if remaining_retries == 0 or not re.match(
                r"^ERROR:1:1: X000 linting with .+ timed out after \d+ seconds",
                err.stdout,
            ):
                raise err
            remaining_retries -= 1
            logging.warning(
                "(%s/%s) Retrying because command failed with: %r",
                retries - remaining_retries,
                retries,
                err,
            )
            time.sleep(1)
