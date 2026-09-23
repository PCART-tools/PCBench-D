def set_faulthander_if_available(_=None):
    faulthandler.enable(sys.__stderr__)
    if not IS_WINDOWS:
        # windows does not have faulthandler.register
        # chain=False prevents the default behavior of killing the process
        faulthandler.register(signal.SIGUSR1, file=sys.__stderr__, chain=False)
