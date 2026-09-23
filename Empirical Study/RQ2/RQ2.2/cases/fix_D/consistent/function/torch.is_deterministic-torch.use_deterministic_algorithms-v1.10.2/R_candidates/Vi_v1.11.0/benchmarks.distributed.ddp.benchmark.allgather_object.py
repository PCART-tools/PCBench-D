def allgather_object(obj):
    out = [None for _ in range(dist.get_world_size())]
    dist.all_gather_object(out, obj)
    return out
