class HashablePartial:
  def __init__(self, f, *args, **kwargs):
    self.f = f
    self.args = args
    self.kwargs = kwargs

  def __eq__(self, other):
    return (type(other) is HashablePartial and
            self.f.__code__ == other.f.__code__ and
            self.args == other.args and self.kwargs == other.kwargs)

  def __hash__(self):
    return hash(
      (
        self.f.__code__,
        self.args,
        tuple(sorted(self.kwargs.items(), key=lambda kv: kv[0])),
      ),
    )

  def __call__(self, *args, **kwargs):
    return self.f(*self.args, *args, **self.kwargs, **kwargs)
