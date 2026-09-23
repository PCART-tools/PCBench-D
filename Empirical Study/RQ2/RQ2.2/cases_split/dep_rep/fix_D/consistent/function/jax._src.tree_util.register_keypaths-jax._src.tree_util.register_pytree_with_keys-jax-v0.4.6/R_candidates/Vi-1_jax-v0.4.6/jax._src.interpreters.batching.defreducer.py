def defreducer(prim):
  primitive_batchers[prim] = partial(reducer_batcher, prim)
