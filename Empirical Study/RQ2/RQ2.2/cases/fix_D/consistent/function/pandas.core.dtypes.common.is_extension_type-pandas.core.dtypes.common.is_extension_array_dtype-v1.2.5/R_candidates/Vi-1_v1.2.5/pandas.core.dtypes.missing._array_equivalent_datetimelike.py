def _array_equivalent_datetimelike(left, right):
    return np.array_equal(left.view("i8"), right.view("i8"))
