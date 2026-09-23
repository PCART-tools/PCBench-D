def create_device(interface=None):
    if sys.platform == "win32" or interface is None:
        return c10d.ProcessGroupGloo.create_device(hostname="127.0.0.1")
    else:
        return c10d.ProcessGroupGloo.create_device(interface=interface)
