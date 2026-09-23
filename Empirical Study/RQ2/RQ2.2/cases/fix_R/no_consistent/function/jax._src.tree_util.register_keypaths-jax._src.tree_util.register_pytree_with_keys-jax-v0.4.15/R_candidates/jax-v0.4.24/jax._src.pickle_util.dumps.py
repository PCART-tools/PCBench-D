@functools.partial(profiler.annotate_function, name='pickle_util.dumps')
def dumps(obj: Any) -> bytes:
  """See `pickle.dumps`. Used for serializing host callbacks in jaxlib."""
  if cloudpickle is None:
    raise ModuleNotFoundError('No module named "cloudpickle"')

  class Pickler(cloudpickle.CloudPickler):
    """Customizes the behavior of cloudpickle."""

    # Make a copy to avoid modifying cloudpickle for other users.
    dispatch_table = cloudpickle.CloudPickler.dispatch_table.copy()

    # Fixes for dataclass internal singleton object serialization.
    # Bug: https://github.com/cloudpipe/cloudpickle/issues/386
    # pylint: disable=protected-access
    # pytype: disable=module-attr
    dispatch_table[dataclasses._FIELD_BASE] = lambda x: f'{x.name}'
    dispatch_table[dataclasses._MISSING_TYPE] = lambda _: 'MISSING'
    dispatch_table[dataclasses._HAS_DEFAULT_FACTORY_CLASS] = (
        lambda _: '_HAS_DEFAULT_FACTORY'
    )
    if hasattr(dataclasses, '_KW_ONLY_TYPE'):
      dispatch_table[dataclasses._KW_ONLY_TYPE] = (
          lambda _: '_KW_ONLY_TYPE'
      )  # Added in Python 3.10.
    # pytype: enable=module-attr
    # pylint: enable=protected-access

  with io.BytesIO() as file:
    Pickler(file).dump(obj)
    return file.getvalue()
