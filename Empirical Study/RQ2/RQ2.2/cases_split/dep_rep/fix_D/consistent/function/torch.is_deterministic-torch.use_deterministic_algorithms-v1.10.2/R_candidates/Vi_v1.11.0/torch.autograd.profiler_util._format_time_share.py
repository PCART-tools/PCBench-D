def _format_time_share(time_us, total_time_us):
    """Defines how to format time in FunctionEvent"""
    if total_time_us == 0:
        assert time_us == 0, "Expected time_us == 0 but got {}".format(time_us)
        return "NaN"
    return '{:.2f}%'.format(time_us * 100.0 / total_time_us)
