def print_json_oss_format(results):
    oss_results = {}
    for group_name, group_val in results.items():
        oss_results[group_name] = {}
        for model_name, run_time in group_val.items():
            # Output for OSS
            oss_results[group_name][model_name] = run_time['avg']

    print(json.dumps(oss_results))
