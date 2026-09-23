def warmup_forward(f, *args, profiling_count=2):
    for i in range(profiling_count):
        results = f(*args)

    return results
