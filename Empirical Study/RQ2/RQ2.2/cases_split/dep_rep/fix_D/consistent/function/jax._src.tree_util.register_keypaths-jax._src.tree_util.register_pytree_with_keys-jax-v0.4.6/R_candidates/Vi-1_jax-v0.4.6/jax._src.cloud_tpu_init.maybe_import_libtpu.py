def maybe_import_libtpu():
  try:
    # pylint: disable=import-outside-toplevel
    # pytype: disable=import-error
    import libtpu

    # pytype: enable=import-error
    # pylint: enable=import-outside-toplevel
  except ImportError:
    return None
  else:
    return libtpu
