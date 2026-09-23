def EuthanizeIfNecessary(timeout_secs=120):
    '''
    Call this if you have problem with process getting stuck at shutdown.
    It will kill the process if it does not terminate in timeout_secs.
    '''
    watcher = WatcherThread(timeout_secs)
    watcher.start()
