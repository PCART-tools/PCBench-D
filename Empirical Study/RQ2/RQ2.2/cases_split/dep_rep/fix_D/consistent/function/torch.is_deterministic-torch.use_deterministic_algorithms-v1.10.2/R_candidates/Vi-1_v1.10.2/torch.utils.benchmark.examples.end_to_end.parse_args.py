def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr", type=str, default=_PR_LIST[0], choices=_PR_LIST)
    parser.add_argument("--num_gpus", type=int, default=None)
    parser.add_argument("--test_variance", action="store_true")

    # (Implementation details)
    parser.add_argument("--DETAIL_context", type=str, choices=(_MAIN, _SUBPROCESS), default=_MAIN)
    parser.add_argument("--DETAIL_device", type=str, choices=(_CPU, _GPU), default=None)
    parser.add_argument("--DETAIL_env", type=str, default=None)
    parser.add_argument("--DETAIL_result_file", type=str, default=None)
    parser.add_argument("--DETAIL_seed", type=int, default=None)

    args = parser.parse_args()
    if args.num_gpus is None:
        args.num_gpus = torch.cuda.device_count()
    return args
