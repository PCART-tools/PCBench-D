def print_json_pep_format(results):
    # print the AI-PEP format json string for each model
    for group_name, group_val in results.items():
        for model_name, run_time in group_val.items():
            # Output for AI-PEP
            num_iters = len(run_time['info'])
            info = run_time['info'].tolist()
            for i in range(num_iters):
                print("Caffe2Observer " + json.dumps(
                    {
                        "type": "NET",
                        "metric": group_name + "-" + model_name,
                        "unit": "ms",
                        "value": str(info[i])
                    }
                ))
