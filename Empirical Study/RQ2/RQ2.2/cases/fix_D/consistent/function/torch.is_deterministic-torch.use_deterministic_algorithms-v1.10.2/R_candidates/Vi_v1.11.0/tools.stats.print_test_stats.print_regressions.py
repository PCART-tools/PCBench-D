def print_regressions(head_report: Report, *, num_prev_commits: int) -> None:
    sha1 = os.environ.get("SHA1", os.environ.get("CIRCLE_SHA1", "HEAD"))

    base = get_base_commit(sha1)

    count_spec = f"{base}..{sha1}"
    intermediate_commits = int(subprocess.check_output(
        ["git", "rev-list", "--count", count_spec],
        encoding="ascii"
    ))
    ancestry_path = int(subprocess.check_output(
        ["git", "rev-list", "--ancestry-path", "--count", count_spec],
        encoding="ascii",
    ))

    # if current commit is already on master, we need to exclude it from
    # this history; otherwise we include the merge-base
    commits = subprocess.check_output(
        ["git", "rev-list", f"--max-count={num_prev_commits+1}", base],
        encoding="ascii",
    ).splitlines()
    on_master = False
    if base == sha1:
        on_master = True
        commits = commits[1:]
    else:
        commits = commits[:-1]

    job = os.environ.get("JOB_BASE_NAME", "")
    objects: Dict[Commit, List[Report]] = defaultdict(list)

    for commit in commits:
        objects[commit]
        summaries = get_test_stats_summaries_for_job(sha=commit, job_prefix=job)
        for _, summary in summaries.items():
            objects[commit].extend(summary)

    print()
    print(regression_info(
        head_sha=sha1,
        head_report=head_report,
        base_reports=objects,
        job_name=job,
        on_master=on_master,
        ancestry_path=ancestry_path - 1,
        other_ancestors=intermediate_commits - ancestry_path,
    ), end="")
