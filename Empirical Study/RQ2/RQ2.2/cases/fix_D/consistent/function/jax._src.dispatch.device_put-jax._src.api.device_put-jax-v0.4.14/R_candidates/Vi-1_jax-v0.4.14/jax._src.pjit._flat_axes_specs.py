def _flat_axes_specs(abstracted_axes, *args, **kwargs
                     ) -> Optional[list[pe.AbstractedAxesSpec]]:
  if abstracted_axes is None: return None
  if kwargs: raise NotImplementedError
  def ax_leaf(l):
    return (isinstance(l, dict) and all_leaves(l.values()) or
            isinstance(l, tuple) and all_leaves(l, lambda x: x is None))
  return broadcast_prefix(abstracted_axes, args, ax_leaf)
