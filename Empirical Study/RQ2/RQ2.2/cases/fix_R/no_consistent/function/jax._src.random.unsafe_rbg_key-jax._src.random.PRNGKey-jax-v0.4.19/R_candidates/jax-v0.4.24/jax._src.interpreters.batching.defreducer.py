def defreducer(prim, ident):
  primitive_batchers[prim] = partial(reducer_batcher, prim, ident)
