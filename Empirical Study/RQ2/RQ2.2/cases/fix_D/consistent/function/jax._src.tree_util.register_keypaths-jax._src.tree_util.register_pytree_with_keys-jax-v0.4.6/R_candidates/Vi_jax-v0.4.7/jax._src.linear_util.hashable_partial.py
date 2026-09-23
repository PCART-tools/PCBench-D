@transformation
def hashable_partial(x, *args):
  ans = yield (x,) + args, {}
  yield ans
