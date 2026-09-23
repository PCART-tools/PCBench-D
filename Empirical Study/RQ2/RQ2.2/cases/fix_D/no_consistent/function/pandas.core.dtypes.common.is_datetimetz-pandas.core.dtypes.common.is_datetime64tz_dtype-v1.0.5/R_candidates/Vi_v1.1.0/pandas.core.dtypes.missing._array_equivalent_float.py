def _array_equivalent_float(left, right):
    return ((left == right) | (np.isnan(left) & np.isnan(right))).all()
