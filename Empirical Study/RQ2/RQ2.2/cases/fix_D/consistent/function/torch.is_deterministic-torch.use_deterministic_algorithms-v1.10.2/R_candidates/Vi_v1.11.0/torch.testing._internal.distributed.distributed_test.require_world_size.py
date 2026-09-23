def require_world_size(world_size):
    if int(os.environ["WORLD_SIZE"]) < world_size:
        return sandcastle_skip("Test requires world size of %d" % world_size)
    return lambda func: func
