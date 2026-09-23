@contextlib.contextmanager
def CompleteInTimeOrDie(timeout_secs):
    watcher = WatcherThread(timeout_secs)
    watcher.start()
    yield
    watcher.completed = True
    watcher.condition.acquire()
    watcher.condition.notify()
    watcher.condition.release()
