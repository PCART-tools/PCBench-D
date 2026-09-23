def in_ipnb():
    """
    check if we're inside an IPython Notebook

    DEPRECATED: This is no longer used in pandas, and won't work in IPython 3
    and above.
    """
    try:
        ip = get_ipython()
        front_end = (
            ip.config.get('KernelApp', {}).get('parent_appname', "") or
            ip.config.get('IPKernelApp', {}).get('parent_appname', "")
        )
        if 'notebook' in front_end.lower():
            return True
    except:
        return False
    return False
