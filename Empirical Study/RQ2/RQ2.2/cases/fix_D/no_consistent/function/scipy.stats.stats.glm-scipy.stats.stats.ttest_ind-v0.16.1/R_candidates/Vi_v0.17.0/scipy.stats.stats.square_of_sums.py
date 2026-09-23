@np.deprecate(message="scipy.stats.square_of_sums is deprecated "
              "in scipy 0.17.0")
def square_of_sums(a, axis=0):
    return _square_of_sums(a, axis)
