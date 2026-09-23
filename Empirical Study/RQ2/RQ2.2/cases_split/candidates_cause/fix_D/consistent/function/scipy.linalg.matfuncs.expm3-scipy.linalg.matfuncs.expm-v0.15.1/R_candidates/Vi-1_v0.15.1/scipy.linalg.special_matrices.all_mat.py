@np.deprecate
def all_mat(*args):
    return list(map(np.matrix, args))
