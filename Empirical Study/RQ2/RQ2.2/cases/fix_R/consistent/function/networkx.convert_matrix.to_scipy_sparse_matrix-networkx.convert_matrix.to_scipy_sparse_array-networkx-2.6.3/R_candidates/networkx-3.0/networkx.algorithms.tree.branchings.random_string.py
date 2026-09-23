@py_random_state(1)
def random_string(L=15, seed=None):
    return "".join([seed.choice(string.ascii_letters) for n in range(L)])
