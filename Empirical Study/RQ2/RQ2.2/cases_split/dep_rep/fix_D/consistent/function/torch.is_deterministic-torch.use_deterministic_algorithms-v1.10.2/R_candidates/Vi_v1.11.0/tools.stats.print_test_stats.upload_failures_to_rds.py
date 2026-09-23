def upload_failures_to_rds(reports: Dict[str, TestFile]) -> None:
    """
    We have 40k+ tests, so saving every test for every commit is not very
    feasible for PyTorch. Most of these are things we don't care about anyways,
    so this code filters out failures and saves only those to the DB.
    """
    # Gather all failures across the entire report
    failures = []
    for file in reports.values():
        for suite in file.test_suites.values():
            for case in suite.test_cases.values():
                if case.errored or case.failed:
                    failures.append({
                        "name": case.name,
                        "suite": suite.name,
                        "file": file.name,
                        "status": "failure" if case.failed else "error"
                    })

    if len(failures) > 0:
        register_rds_schema("test_failures", schema_from_sample(failures[0]))
        rds_write("test_failures", failures, only_on_master=False)
