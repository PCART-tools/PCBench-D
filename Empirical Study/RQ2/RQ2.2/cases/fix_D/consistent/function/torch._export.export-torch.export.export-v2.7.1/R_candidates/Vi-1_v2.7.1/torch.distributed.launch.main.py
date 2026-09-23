@_deprecated(
    "The module torch.distributed.launch is deprecated\n"
    "and will be removed in future. Use torchrun.\n"
    "Note that --use-env is set by default in torchrun.\n"
    "If your script expects `--local-rank` argument to be set, please\n"
    "change it to read from `os.environ['LOCAL_RANK']` instead. See \n"
    "https://pytorch.org/docs/stable/distributed.html#launch-utility for \n"
    "further instructions\n",
    category=FutureWarning,
)
def main(args=None):
    args = parse_args(args)
    launch(args)
