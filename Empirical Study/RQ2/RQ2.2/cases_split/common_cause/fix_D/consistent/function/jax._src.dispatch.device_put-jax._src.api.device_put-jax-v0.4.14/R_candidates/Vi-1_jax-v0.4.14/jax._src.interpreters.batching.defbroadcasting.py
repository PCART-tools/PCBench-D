def defbroadcasting(prim):
  primitive_batchers[prim] = partial(broadcast_batcher, prim)
