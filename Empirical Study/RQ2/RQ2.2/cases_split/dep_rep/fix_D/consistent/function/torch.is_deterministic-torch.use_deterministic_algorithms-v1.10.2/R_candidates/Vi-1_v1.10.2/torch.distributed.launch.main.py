def main(args=None):
    warnings.warn(
        "The module torch.distributed.launch is deprecated\n"
        "and will be removed in future. Use torchrun.\n"
        "Note that --use_env is set by default in torchrun.\n"
        "If your script expects `--local_rank` argument to be set, please\n"
        "change it to read from `os.environ['LOCAL_RANK']` instead. See \n"
        "https://pytorch.org/docs/stable/distributed.html#launch-utility for \n"
        "further instructions\n",
        FutureWarning,
    )
    args = parse_args(args)
    launch(args)
