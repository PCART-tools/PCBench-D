def this_before_that_pass_constraint(this: Callable, that: Callable):
    """
    Defines a partial order ('depends on' function) where `this` must occur
    before `that`.
    """

    def depends_on(a: Callable, b: Callable):
        return a != that or b != this

    return depends_on
