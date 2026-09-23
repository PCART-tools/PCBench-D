def _get_role_info() -> RankInfo:
    rank = int(os.environ["RANK"])
    role_rank = int(os.environ["ROLE_RANK"])
    group_rank = int(os.environ["GROUP_RANK"])
    role_world_size = int(os.environ["ROLE_WORLD_SIZE"])
    world_size = int(os.environ["WORLD_SIZE"])
    return RankInfo(rank, role_rank, group_rank, role_world_size, world_size)
