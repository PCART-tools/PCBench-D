def wrap_nvcc(
    args: List[str],
    config: argparse.Namespace = default_config,
) -> int:
    return subprocess.call([config.nvcc] + args)
