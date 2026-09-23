def defvectorized(prim):
  primitive_batchers[prim] = partial(vectorized_batcher, prim)
