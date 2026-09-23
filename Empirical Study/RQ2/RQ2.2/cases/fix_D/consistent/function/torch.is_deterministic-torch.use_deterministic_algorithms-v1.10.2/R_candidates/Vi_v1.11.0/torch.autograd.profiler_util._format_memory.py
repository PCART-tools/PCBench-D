def _format_memory(nbytes):
    """Returns a formatted memory size string"""
    KB = 1024
    MB = 1024 * KB
    GB = 1024 * MB
    if (abs(nbytes) >= GB):
        return '{:.2f} Gb'.format(nbytes * 1.0 / GB)
    elif (abs(nbytes) >= MB):
        return '{:.2f} Mb'.format(nbytes * 1.0 / MB)
    elif (abs(nbytes) >= KB):
        return '{:.2f} Kb'.format(nbytes * 1.0 / KB)
    else:
        return str(nbytes) + ' b'
