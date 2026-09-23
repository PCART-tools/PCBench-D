def _print(msg):
    if dist.get_rank() == 0:
        print(msg)
