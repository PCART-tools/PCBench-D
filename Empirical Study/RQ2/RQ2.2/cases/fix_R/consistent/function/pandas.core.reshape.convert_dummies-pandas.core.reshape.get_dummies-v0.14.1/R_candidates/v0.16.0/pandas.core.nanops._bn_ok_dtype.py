def _bn_ok_dtype(dt, name):
    # Bottleneck chokes on datetime64
    if (not is_object_dtype(dt) and
            not is_datetime_or_timedelta_dtype(dt)):

        # bottleneck does not properly upcast during the sum
        # so can overflow
        if name == 'nansum':
            if dt.itemsize < 8:
                return False

        return True
    return False
