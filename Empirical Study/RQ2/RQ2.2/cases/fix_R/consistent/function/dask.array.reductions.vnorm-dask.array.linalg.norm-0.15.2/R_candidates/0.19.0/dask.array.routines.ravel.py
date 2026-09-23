@wraps(np.ravel)
def ravel(array):
    return array.reshape((-1,))
