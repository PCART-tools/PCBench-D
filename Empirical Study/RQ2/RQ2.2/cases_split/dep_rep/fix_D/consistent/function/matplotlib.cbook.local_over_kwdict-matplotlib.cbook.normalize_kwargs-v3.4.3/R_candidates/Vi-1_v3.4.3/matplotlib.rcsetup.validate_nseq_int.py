@_api.deprecated("3.3")
def validate_nseq_int(n):
    return _make_nseq_validator(int, n)
