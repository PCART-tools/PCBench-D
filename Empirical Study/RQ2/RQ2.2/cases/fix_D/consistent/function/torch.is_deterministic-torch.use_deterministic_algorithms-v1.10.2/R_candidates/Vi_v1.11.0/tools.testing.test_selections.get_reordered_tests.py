def get_reordered_tests(tests: List[str], is_reordering_by_pr: bool) -> List[str]:
    """Get the reordered test filename list based on github PR history or git changed file.
    """
    prioritized_tests = []
    # Try using historic stats from PR.
    if is_reordering_by_pr and HAVE_BOTO3:
        pr_number = os.environ.get("PR_NUMBER", os.environ.get("CIRCLE_PR_NUMBER", ""))
        if len(pr_number):
            ci_job_prefix = _get_stripped_CI_job()
            s3_reports: List[Tuple["Report", str]] = get_previous_reports_for_pr(
                pr_number, ci_job_prefix)
            prioritized_tests = _query_failure_test_module(s3_reports)
            print("Prioritized test from previous CI info.")

    # Using file changes priority if no stats found from previous PR.
    if len(prioritized_tests) == 0:
        try:
            changed_files = _query_changed_test_files()
        except Exception:
            # If unable to get changed files from git, quit without doing any sorting
            return tests

        prefix = f"test{os.path.sep}"
        prioritized_tests = [f for f in changed_files if f.startswith(prefix) and f.endswith(".py")]
        prioritized_tests = [f[len(prefix):] for f in prioritized_tests]
        prioritized_tests = [f[:-len(".py")] for f in prioritized_tests]
        print("Prioritized test from test file changes.")

    bring_to_front = []
    the_rest = []

    for test in tests:
        if test in prioritized_tests:
            bring_to_front.append(test)
        else:
            the_rest.append(test)
    if len(tests) == len(bring_to_front) + len(the_rest):
        print(f"reordering tests for PR:\n"
              f"prioritized: {bring_to_front}\nthe rest: {the_rest}\n")
        return bring_to_front + the_rest
    else:
        print(f"Something went wrong in CI reordering, expecting total of {len(tests)}:\n"
              f"but found prioritized: {len(bring_to_front)}\nthe rest: {len(the_rest)}\n")
        return tests
