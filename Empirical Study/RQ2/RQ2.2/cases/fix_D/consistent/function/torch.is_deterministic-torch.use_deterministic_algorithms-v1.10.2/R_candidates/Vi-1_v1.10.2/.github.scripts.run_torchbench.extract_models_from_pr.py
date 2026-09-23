def extract_models_from_pr(torchbench_path: str, prbody_file: str) -> List[str]:
    model_list = []
    with open(prbody_file, "r") as pf:
        lines = map(lambda x: x.strip(), pf.read().splitlines())
        magic_lines = list(filter(lambda x: x.startswith(MAGIC_PREFIX), lines))
        if magic_lines:
            # Only the first magic line will be recognized.
            model_list = list(map(lambda x: x.strip(), magic_lines[0][len(MAGIC_PREFIX):].split(",")))
    # Shortcut: if model_list is ["ALL"], run all the tests
    if model_list == ["ALL"]:
        return model_list
    # Sanity check: make sure all the user specified models exist in torchbench repository
    benchmark_path = os.path.join(torchbench_path, "torchbenchmark", "models")
    full_model_list = [model for model in os.listdir(benchmark_path) if os.path.isdir(os.path.join(benchmark_path, model))]
    for m in model_list:
        if m not in full_model_list:
            print(f"The model {m} you specified does not exist in TorchBench suite. Please double check.")
            return []
    return model_list
