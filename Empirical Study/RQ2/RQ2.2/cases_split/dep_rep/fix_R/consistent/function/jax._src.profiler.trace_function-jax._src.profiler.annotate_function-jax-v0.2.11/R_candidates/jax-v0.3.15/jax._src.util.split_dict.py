def split_dict(dct, names):
  dct = dict(dct)
  lst = [dct.pop(name) for name in names]
  assert not dct
  return lst
