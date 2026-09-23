def _new_Index(cls, d):
    """ This is called upon unpickling, rather than the default which doesn't have arguments
        and breaks __new__ """
    return cls.__new__(cls, **d)
