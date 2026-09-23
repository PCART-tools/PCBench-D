@functools.partial(profiler.annotate_function, name='pickle_util.loads')
def loads(data: bytes) -> Any:
  """See `pickle.loads`."""
  if cloudpickle is None:
    raise ModuleNotFoundError('No module named "cloudpickle"')

  return cloudpickle.loads(data)
