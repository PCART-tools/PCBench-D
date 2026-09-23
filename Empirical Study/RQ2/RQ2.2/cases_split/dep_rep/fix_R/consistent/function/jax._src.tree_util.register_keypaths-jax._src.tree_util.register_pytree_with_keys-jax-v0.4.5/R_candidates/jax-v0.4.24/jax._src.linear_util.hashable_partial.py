@transformation
def hashable_partial(*args):
  yield (yield args, {})
