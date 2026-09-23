def add_tensors_loop(x, y):
    z = torch.add(x, y)
    for i in range(NUM_LOOP_ITERS):
        z = torch.add(z, x)
    return z
