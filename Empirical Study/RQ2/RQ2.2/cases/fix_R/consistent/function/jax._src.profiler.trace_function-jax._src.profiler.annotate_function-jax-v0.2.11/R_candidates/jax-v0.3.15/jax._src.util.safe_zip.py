def safe_zip(*args):
  n = len(args[0])
  for arg in args[1:]:
    assert len(arg) == n, f'length mismatch: {list(map(len, args))}'
  return list(zip(*args))
