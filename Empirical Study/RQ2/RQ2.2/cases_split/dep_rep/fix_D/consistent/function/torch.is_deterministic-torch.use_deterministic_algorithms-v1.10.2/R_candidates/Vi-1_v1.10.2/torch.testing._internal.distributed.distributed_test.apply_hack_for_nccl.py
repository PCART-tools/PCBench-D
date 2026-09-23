def apply_hack_for_nccl():
    # This is a hack for a known NCCL issue using multiprocess
    # in conjunction with multiple threads to manage different GPUs which
    # may cause ncclCommInitRank to fail.
    # http://docs.nvidia.com/deeplearning/sdk/nccl-release-notes/rel_2.1.4.html#rel_2.1.4
    # It slows down the performance of collective operations.
    # Without this setting NCCL might throw unhandled error.
    os.environ["NCCL_MAX_NRINGS"] = "1"
