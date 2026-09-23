def _array_equivalent_datetimelike(left: np.ndarray, right: np.ndarray):
    return np.array_equal(left.view("i8"), right.view("i8"))
