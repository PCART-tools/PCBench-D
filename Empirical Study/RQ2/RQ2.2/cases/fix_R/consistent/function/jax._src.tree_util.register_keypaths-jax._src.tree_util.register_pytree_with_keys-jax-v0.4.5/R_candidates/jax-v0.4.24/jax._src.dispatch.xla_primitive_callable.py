@util.cache()
def xla_primitive_callable(prim: core.Primitive, **params):
  def prim_fun(*args):
    return prim.bind(*args, **params)
  prim_fun.__name__ = prim.name
  prim_fun.__qualname__ = prim.name
  return api.jit(prim_fun)
