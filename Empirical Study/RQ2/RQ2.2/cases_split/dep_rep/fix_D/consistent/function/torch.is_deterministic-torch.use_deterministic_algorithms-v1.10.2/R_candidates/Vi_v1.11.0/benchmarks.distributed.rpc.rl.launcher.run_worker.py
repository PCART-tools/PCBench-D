def run_worker(rank, world_size, master_addr, master_port, batch, state_size, nlayers, out_features, queue):
    r"""
    inits an rpc worker
    Args:
        rank (int): Rpc rank of worker machine
        world_size (int): Number of workers in rpc network (number of observers +
                          1 agent + 1 coordinator)
        master_addr (str): Master address of cooridator
        master_port (str): Master port of coordinator
        batch (bool): Whether agent will use batching or process one observer
                      request a at a time
        state_size (str): Numerical str representing state dimensions (ie: 5-15-10)
        nlayers (int): Number of layers in model
        out_features (int): Number of out features in model
        queue (SimpleQueue): SimpleQueue from torch.multiprocessing.get_context() for
                             saving benchmark run results to
    """
    state_size = list(map(int, state_size.split('-')))
    batch_size = world_size - 2  # No. of observers

    os.environ['MASTER_ADDR'] = master_addr
    os.environ['MASTER_PORT'] = master_port
    if rank == 0:
        rpc.init_rpc(COORDINATOR_NAME, rank=rank, world_size=world_size)

        coordinator = CoordinatorBase(
            batch_size, batch, state_size, nlayers, out_features)
        coordinator.run_coordinator(TOTAL_EPISODES, TOTAL_EPISODE_STEPS, queue)

    elif rank == 1:
        rpc.init_rpc(AGENT_NAME, rank=rank, world_size=world_size)
    else:
        rpc.init_rpc(OBSERVER_NAME.format(rank),
                     rank=rank, world_size=world_size)
    rpc.shutdown()
