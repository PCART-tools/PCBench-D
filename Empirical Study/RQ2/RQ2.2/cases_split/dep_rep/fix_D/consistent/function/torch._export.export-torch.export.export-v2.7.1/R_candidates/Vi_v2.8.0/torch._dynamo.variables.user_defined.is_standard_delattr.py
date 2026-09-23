def is_standard_delattr(val):
    return val in (object.__delattr__, BaseException.__delattr__)
