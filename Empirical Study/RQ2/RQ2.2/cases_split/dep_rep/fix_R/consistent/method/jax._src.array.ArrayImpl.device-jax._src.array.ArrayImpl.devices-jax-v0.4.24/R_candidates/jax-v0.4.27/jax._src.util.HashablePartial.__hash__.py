  def __hash__(self):
    return hash(
      (
        self.f.__code__,
        self.args,
        tuple(sorted(self.kwargs.items(), key=lambda kv: kv[0])),
      ),
    )
