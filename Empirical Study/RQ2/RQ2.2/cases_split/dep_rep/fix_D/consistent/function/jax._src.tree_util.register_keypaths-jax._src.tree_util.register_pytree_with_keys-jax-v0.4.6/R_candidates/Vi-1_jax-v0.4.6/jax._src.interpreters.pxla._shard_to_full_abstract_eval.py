@shard_to_full_p.def_abstract_eval
def _shard_to_full_abstract_eval(x, axes, mesh, **_):
  # TODO: Assert x is a global aval! Or ideally check that it's global in dims from axes!
  return untile_aval_nd(mesh.shape, axes, x)
