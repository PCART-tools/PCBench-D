@wraps(np.ravel)
def ravel(array):
    return reshape(array, (-1,))
