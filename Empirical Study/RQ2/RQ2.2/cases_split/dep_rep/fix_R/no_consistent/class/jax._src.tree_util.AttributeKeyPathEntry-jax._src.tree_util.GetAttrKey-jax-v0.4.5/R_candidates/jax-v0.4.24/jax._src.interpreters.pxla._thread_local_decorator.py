class _thread_local_decorator(threading.local):

  def __init__(self, fn):
    self.fn = fn

  def __call__(self, *args, **kwargs):
    return self.fn(*args, **kwargs)
