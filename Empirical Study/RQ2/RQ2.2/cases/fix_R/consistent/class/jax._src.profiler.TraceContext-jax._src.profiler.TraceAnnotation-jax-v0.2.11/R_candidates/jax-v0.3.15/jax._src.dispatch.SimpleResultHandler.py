class SimpleResultHandler:
  handlers: Sequence[ResultHandler]
  def __init__(self, handlers): self.handlers = handlers
  def __iter__(self): return iter(self.handlers)
  def __len__(self): return len(self.handlers)
  def __call__(self, env, lists_of_bufs):
    return tuple(h(env, *bs) for h, bs in zip(self.handlers, lists_of_bufs))
