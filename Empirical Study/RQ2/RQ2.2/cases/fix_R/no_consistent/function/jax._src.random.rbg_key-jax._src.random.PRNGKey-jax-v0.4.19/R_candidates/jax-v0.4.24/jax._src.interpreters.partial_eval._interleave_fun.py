@lu.transformation
def _interleave_fun(every_others, *args, **kwargs):
  args_ = [x for pair in zip(args, every_others) for x in pair]
  yield (yield (args_, kwargs))
