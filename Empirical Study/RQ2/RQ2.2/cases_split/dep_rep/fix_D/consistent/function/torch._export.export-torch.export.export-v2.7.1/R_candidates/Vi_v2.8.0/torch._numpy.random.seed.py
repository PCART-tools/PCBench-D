@deco_stream
def seed(seed=None):
    if seed is not None:
        torch.random.manual_seed(seed)
