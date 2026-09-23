def in_qtconsole():
    """
    check if we're inside an IPython qtconsole

    DEPRECATED: This is no longer needed, or working, in IPython 3 and above.
    """
    try:
        ip = get_ipython()
        front_end = (
            ip.config.get('KernelApp', {}).get('parent_appname', "") or
            ip.config.get('IPKernelApp', {}).get('parent_appname', "")
        )
        if 'qtconsole' in front_end.lower():
            return True
    except:
        return False
    return False
