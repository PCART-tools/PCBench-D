@lu.transformation
def vtile_manual(manual_axes: FrozenSet[MeshAxisName],
                 mesh: Mesh,
                 in_axes: Sequence[ArrayMapping],
                 out_axes: Sequence[ArrayMapping],
                 *args):
  tiled_args = [full_to_shard_p.bind(arg, axes=axes, mesh=mesh, manual_axes=manual_axes)
                for arg, axes in zip(args, in_axes)]
  tiled_outs = yield tiled_args, {}
  outs = [shard_to_full_p.bind(out, axes=axes, mesh=mesh, manual_axes=manual_axes)
          for out, axes in zip(tiled_outs, out_axes)]
  yield outs
