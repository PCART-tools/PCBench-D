@full_to_shard_p.def_abstract_eval
def _full_to_shard_abstract_eval(x, axes, mesh, **_):
  # TODO: Assert x is a global aval! Or ideally check that it's global in dims from axes!
  return tile_aval_nd(mesh.shape, axes, x)
