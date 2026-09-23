def is_standard_setattr(val):
    return val in (object.__setattr__, BaseException.__setattr__)
