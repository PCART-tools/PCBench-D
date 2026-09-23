def assemble_flaky_test_stats(duplicated_tests_by_file: Dict[str, DuplicatedDict]) -> Any:
    flaky_tests = []
    workflow_id = os.environ.get("GITHUB_RUN_ID", os.environ.get("CIRCLE_WORKFLOW_ID", None))
    for file_name, suite_to_dict in duplicated_tests_by_file.items():
        for suite_name, testcase_to_runs in suite_to_dict.items():
            for testcase_name, list_of_runs in testcase_to_runs.items():
                num_green, num_red = process_intentional_test_runs(list_of_runs)
                if num_green > 0:   # Otherwise, it's likely just a failing test
                    flaky_tests.append({
                        "name": testcase_name,
                        "suite": suite_name,
                        "file": file_name,
                        "num_green": num_green,
                        "num_red": num_red,
                    })
    if len(flaky_tests) > 0:
        # write to RDS
        register_rds_schema("flaky_tests", schema_from_sample(flaky_tests[0]))
        rds_write("flaky_tests", flaky_tests, only_on_master=False)

        # write to S3 to go to Rockset as well
        import uuid
        for flaky_test in flaky_tests:
            flaky_test["workflow_id"] = workflow_id
            key = f"flaky_tests/{workflow_id}/{uuid.uuid4()}.json"
            obj = get_S3_object_from_bucket("ossci-raw-job-status", key)
            obj.put(Body=json.dumps(flaky_test), ContentType="application/json")
