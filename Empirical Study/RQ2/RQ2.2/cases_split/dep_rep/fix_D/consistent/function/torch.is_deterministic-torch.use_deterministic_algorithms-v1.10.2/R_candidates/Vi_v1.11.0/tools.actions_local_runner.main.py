def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pull shell scripts out of GitHub actions and run them"
    )
    parser.add_argument("--file", help="YAML file with actions")
    parser.add_argument(
        "--changed-only",
        help="only run on changed files",
        action="store_true",
        default=False,
    )
    parser.add_argument("--job", help="job name", required=True)
    parser.add_argument(
        "--no-quiet", help="output commands", action="store_true", default=False
    )
    parser.add_argument("--step", action="append", help="steps to run (in order)")
    args = parser.parse_args()

    quiet = not args.no_quiet

    if args.file is None:
        # If there is no .yml file provided, fall back to the list of known
        # jobs. We use this for flake8 and mypy since they run different
        # locally than in CI due to 'make quicklint'
        if args.job not in ad_hoc_steps:
            raise RuntimeError(
                f"Job {args.job} not found and no .yml file was provided"
            )

        files = None
        if args.changed_only:
            files = changed_files()

        checks = [ad_hoc_steps[args.job](files, quiet)]
    else:
        if args.step is None:
            raise RuntimeError("1+ --steps must be provided")

        action = yaml.safe_load(open(args.file, "r"))
        if "jobs" not in action:
            raise RuntimeError(f"top level key 'jobs' not found in {args.file}")
        jobs = action["jobs"]

        if args.job not in jobs:
            raise RuntimeError(f"job '{args.job}' not found in {args.file}")

        job = jobs[args.job]

        # Pull the relevant sections out of the provided .yml file and run them
        relevant_steps = grab_specific_steps(args.step, job)
        checks = [
            YamlStep(step=step, job_name=args.job, quiet=quiet)
            for step in relevant_steps
        ]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*[check.run() for check in checks]))
