def is_valid_mm_plus_mm(match: Match):
    if not torch._inductor.utils.use_max_autotune():
        return False

    *_b1, m1, k1 = match.kwargs["mat1"].meta.get("tensor_meta").shape
    *_b2, k2, n1 = match.kwargs["mat2"].meta.get("tensor_meta").shape
    if k1 != k2:
        return False

    *_b1, m2, k3 = match.kwargs["mat3"].meta.get("tensor_meta").shape
    *_b2, k4, n2 = match.kwargs["mat4"].meta.get("tensor_meta").shape
    if k3 != k4:
        return False

    if m1 != m2 or n1 != n2:
        return False

    return True
