def in_ipython_frontend():
    """
    check if we're inside an an IPython zmq frontend
    """
    try:
        ip = get_ipython()
        return 'zmq' in str(type(ip)).lower()
    except:
        pass

    return False
