def _array_equivalent_float(left, right) -> bool:
    return bool(((left == right) | (np.isnan(left) & np.isnan(right))).all())
