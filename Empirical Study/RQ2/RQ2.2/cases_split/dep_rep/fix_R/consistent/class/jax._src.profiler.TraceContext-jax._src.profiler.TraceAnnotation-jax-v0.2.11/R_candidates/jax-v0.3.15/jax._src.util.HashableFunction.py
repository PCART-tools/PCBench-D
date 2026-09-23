class HashableFunction:
  """Decouples function equality and hash from its identity.

  Local lambdas and functiond defs are reallocated on each function call, making
  the functions created on different calls compare as unequal. This breaks our
  caching logic, which should really only care about comparing the semantics and
  not actual identity.

  This class makes it possible to compare different functions based on their
  semantics. The parts that are taken into account are: the bytecode of
  the wrapped function (which is cached by the CPython interpreter and is stable
  across the invocations of the surrounding function), and `closure` which should
  contain all values in scope that affect the function semantics. In particular
  `closure` should contain all elements of the function closure, or it should be
  possible to derive the relevant elements of the true function closure based
  solely on the contents of the `closure` argument (e.g. in case some closed-over
  values are not hashable, but are entirely determined by hashable locals).
  """

  def __init__(self, f, closure):
    self.f = f
    self.closure = closure

  def __eq__(self, other):
    return (type(other) is HashableFunction and
            self.f.__code__ == other.f.__code__ and
            self.closure == other.closure)

  def __hash__(self):
    return hash((self.f.__code__, self.closure))

  def __call__(self, *args, **kwargs):
    return self.f(*args, **kwargs)

  def __repr__(self):
    return f'<hashable {self.f.__name__} with closure={self.closure}>'
