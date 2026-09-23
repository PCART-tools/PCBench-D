def get_n_rand_nums(min_val, max_val, n):
    random.seed((1 << 32) - 1)
    return random.sample(range(min_val, max_val), n)
