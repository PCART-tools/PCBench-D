def reverse_sequential_wrapper2(sequential):
    """ Given a sequential class for two modules, return a function that takes
    is_qat, and then two modules as argument, that ignores the is_qat flag
    and always returns the sequential that combines the two input modules, with
    the order of two inputs reversed
    """
    def fuser_method(is_qat, m1, m2):
        return sequential(m2, m1)
    return fuser_method
