def format_time(time_us=None, time_ms=None, time_s=None):
    '''Defines how to format time'''
    assert sum([time_us is not None, time_ms is not None, time_s is not None]) == 1

    US_IN_SECOND = 1e6
    US_IN_MS = 1e3

    if time_us is None:
        if time_ms is not None:
            time_us = time_ms * US_IN_MS
        elif time_s is not None:
            time_us = time_s * US_IN_SECOND
        else:
            raise AssertionError("Shouldn't reach here :)")

    if time_us >= US_IN_SECOND:
        return '{:.3f}s'.format(time_us / US_IN_SECOND)
    if time_us >= US_IN_MS:
        return '{:.3f}ms'.format(time_us / US_IN_MS)
    return '{:.3f}us'.format(time_us)
