def run(
    *,
    args: List[str],
    files: List[str],
) -> Tuple[int, List[str], List[str]]:
    """
    Return the exit code and list of output lines from running `mypy`.

    The given `args` are passed verbatim to `mypy`. The `files` (each of
    which must be an absolute path) are converted to relative paths
    (that is, relative to the root of this repo) and then classified
    according to which ones need to be run with each `mypy` config.
    Thus, `mypy` may be run zero, one, or multiple times, but it will be
    run at most once for each `mypy` config used by this repo.
    """
    repo_root = Path.cwd()
    plan = make_plan(configs=config_files(), files=[
        PurePath(f).relative_to(repo_root).as_posix() for f in files
    ])
    mypy_results = [
        mypy.api.run(
            # insert custom flags after args to avoid being overridden
            # by existing flags in args
            args + [
                # don't special-case the last line
                '--no-error-summary',
                f'--config-file={config}',
            ] + filtered
        )
        # by construction, filtered must be nonempty
        for config, filtered in plan.items()
    ]
    return (
        # assume all mypy exit codes are nonnegative
        # https://github.com/python/mypy/issues/6003
        max(
            [exit_code for _, _, exit_code in mypy_results],
            default=0,
        ),
        list(dict.fromkeys(  # remove duplicates, retain order
            item
            for stdout, _, _ in mypy_results
            for item in stdout.splitlines()
        )),
        [stderr for _, stderr, _ in mypy_results],
    )
