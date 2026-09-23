def init_random_seed(seed: int):
    import numpy

    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    numpy.random.seed(seed)
