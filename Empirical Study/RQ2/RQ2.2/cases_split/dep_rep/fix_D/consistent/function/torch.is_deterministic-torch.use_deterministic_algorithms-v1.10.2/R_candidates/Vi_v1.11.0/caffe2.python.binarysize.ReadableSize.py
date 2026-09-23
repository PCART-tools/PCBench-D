def ReadableSize(num):
    """Get a human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(num) <= 1024.0:
            return '%3.2f%s' % (num, unit)
        num /= 1024.0
    return '%.1f TB' % (num,)
