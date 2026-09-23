def get_previous_reports_for_branch(branch: str, ci_job_prefix: str = "") -> List[Report]:
    commit_date_ts = subprocess.check_output(
        ['git', 'show', '-s', '--format=%ct', 'HEAD'],
        encoding="ascii").strip()
    commit_date = datetime.fromtimestamp(int(commit_date_ts))
    # We go a day before this current commit to avoiding pulling incomplete reports
    day_before_commit = str(commit_date - timedelta(days=1)).split(' ')[0]
    # something like git rev-list --before="2021-03-04" --max-count=10 --remotes="*origin/nightly"
    commits = subprocess.check_output(
        ["git", "rev-list", f"--before={day_before_commit}", "--max-count=10", f"--remotes=*{branch}"],
        encoding="ascii").splitlines()

    reports: List[Report] = []
    commit_index = 0
    while len(reports) == 0 and commit_index < len(commits):
        commit = commits[commit_index]
        logger.info(f'Grabbing reports from commit: {commit}')
        summaries = get_test_stats_summaries_for_job(sha=commit, job_prefix=ci_job_prefix)
        for job_name, summary in summaries.items():
            reports.append(summary[0])
            if len(summary) > 1:
                logger.warning(f'WARNING: Multiple summary objects found for {commit}/{job_name}')
        commit_index += 1
    return reports
