def _dot_with_type_promotion(u, v):
    assert u.dim() == 1 and v.dim() == 1
    return (u * v).sum()
