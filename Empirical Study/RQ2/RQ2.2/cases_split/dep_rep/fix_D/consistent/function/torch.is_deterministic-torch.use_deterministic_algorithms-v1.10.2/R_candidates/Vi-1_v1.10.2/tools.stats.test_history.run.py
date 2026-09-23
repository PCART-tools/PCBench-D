def run(raw: List[str]) -> Iterator[str]:
    args = parse_args(raw)

    commits = get_git_commit_history(path=args.pytorch, ref=args.ref)

    return history_lines(
        commits=commits,
        jobs=args.jobs,
        filename=args.file,
        suite_name=args.suite,
        test_name=args.test,
        delta=args.delta,
        mode=args.mode,
        sha_length=args.sha_length,
        digits=args.digits,
    )
