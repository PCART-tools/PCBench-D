def deploy_torchbench_config(output_dir: str, config: str) -> None:
    # Create test dir if needed
    pathlib.Path(output_dir).mkdir(exist_ok=True)
    # TorchBench config file name
    config_path = os.path.join(output_dir, TORCHBENCH_CONFIG_NAME)
    with open(config_path, "w") as fp:
        fp.write(config)
