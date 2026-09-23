def init_rpc(name, backend):
    rank = int(os.environ["RANK"])
    world_size = int(os.environ["WORLD_SIZE"])
    rpc.init_rpc(
        name=name,
        backend=backend,
        rank=rank,
        world_size=world_size,
    )
