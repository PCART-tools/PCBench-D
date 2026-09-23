def init_multigpu_helper(world_size: int, backend: str):
    """Multigpu tests are designed to simulate the multi nodes with multi
    GPUs on each node. Nccl backend requires equal #GPUs in each process.
    On a single node, all visible GPUs are evenly
    divided to subsets, each process only uses a subset.
    """
    nGPUs = torch.cuda.device_count()
    visible_devices = range(nGPUs)

    if backend == "nccl":
        # This is a hack for a known NCCL issue using multiprocess
        # in conjunction with multiple threads to manage different GPUs which
        # may cause ncclCommInitRank to fail.
        # http://docs.nvidia.com/deeplearning/sdk/nccl-release-notes/rel_2.1.4.html#rel_2.1.4
        # It slows down the performance of collective operations.
        # Without this setting NCCL might throw unhandled error.
        os.environ["NCCL_MAX_NRINGS"] = "1"

    # If rank is less than or equal to number of available GPU's
    # then each rank can be mapped to corresponding GPU.
    nGPUs_per_process = 1
    if world_size > nGPUs:
        nGPUs_per_process = nGPUs // world_size
    rank_to_GPU = {
        i: list(
            visible_devices[i * nGPUs_per_process : (i + 1) * nGPUs_per_process]
        )
        for i in range(world_size)
    }
    return rank_to_GPU
