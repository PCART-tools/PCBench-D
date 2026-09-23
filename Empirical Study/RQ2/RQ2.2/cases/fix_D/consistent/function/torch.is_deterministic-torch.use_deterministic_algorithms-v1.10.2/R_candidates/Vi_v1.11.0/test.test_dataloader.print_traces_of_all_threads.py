def print_traces_of_all_threads(pid):
    if not IS_WINDOWS:
        # use the custom signal if available
        os.kill(pid, signal.SIGUSR1)
    else:
        # otherwise we can still use the handler given by faulthandler.enable()
        # at the cost of killing the process.
        os.kill(pid, signal.SIGSEGV)

    # wait in parent process to give subprocess some time to print
    time.sleep(5)
