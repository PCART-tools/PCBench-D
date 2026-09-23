def _construct_result(left, result, index, name, dtype):
    return left._constructor(result, index=index, name=name, dtype=dtype)
