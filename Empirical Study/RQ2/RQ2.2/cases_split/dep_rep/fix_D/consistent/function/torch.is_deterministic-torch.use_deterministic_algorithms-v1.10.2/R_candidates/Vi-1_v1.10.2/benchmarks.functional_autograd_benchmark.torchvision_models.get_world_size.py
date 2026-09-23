def get_world_size():
    if not is_dist_avail_and_initialized():
        return 1
