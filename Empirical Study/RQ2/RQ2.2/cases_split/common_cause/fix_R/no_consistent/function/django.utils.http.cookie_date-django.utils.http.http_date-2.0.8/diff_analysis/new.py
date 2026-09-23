def cookie_date(epoch_seconds=None):
    """
    Format the time to ensure compatibility with Netscape's cookie standard.

    `epoch_seconds` is a floating point number expressed in seconds since the
    epoch, in UTC - such as that outputted by time.time(). If set to None, it
    defaults to the current time.

    Output a string in the format 'Wdy, DD-Mon-YYYY HH:MM:SS GMT'.
    """
    warnings.warn(
        'cookie_date() is deprecated in favor of http_date(), which follows '
        'the format of the latest RFC.',
        RemovedInDjango30Warning, stacklevel=2,
    )
    rfcdate = formatdate(epoch_seconds)
    return '%s-%s-%s GMT' % (rfcdate[:7], rfcdate[8:11], rfcdate[12:25])
