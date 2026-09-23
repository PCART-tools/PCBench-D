def keystr(keys: KeyPath):
  """Helper to pretty-print a tuple of keys.

  Args:
    keys: A tuple of ``KeyEntry`` or any class that can be converted to string.

  Returns:
    A string that joins all string representations of the keys.
  """
  return ''.join([str(k) for k in keys])
