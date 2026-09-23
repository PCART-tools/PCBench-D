class _ThreadLocalStateCache(threading.local):
  """"A thread local cache for _ThreadLocalExtraJitContext

  The extra_jit_context in jax_jit.thread_local_state() may get updated and thus
  incurring dispatch overhead for comparing this python object during jit calls.
  We want to duduplicate the objects that have the same hash/equality to also
  have the same object ID, since the equality check is much faster if the object
  IDs match.
  """
  def __init__(self):
    self.canonicalize = functools.lru_cache(128)(lambda x: x)
