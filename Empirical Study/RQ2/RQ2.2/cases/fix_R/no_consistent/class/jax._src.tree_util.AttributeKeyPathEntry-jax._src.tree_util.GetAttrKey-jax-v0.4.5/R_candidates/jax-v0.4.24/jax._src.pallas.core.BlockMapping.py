@dataclasses.dataclass(frozen=True)
class BlockMapping:
  block_shape: tuple[Mapped | int, ...]
  index_map_jaxpr: jax_core.ClosedJaxpr

  def compute_start_indices(self, loop_idx, *args):
    discharged_jaxpr, discharged_consts = state_discharge.discharge_state(
        self.index_map_jaxpr.jaxpr, self.index_map_jaxpr.consts
    )
    jaxpr = jax_core.ClosedJaxpr(discharged_jaxpr, discharged_consts)
    block_indices_and_rest = jax_core.jaxpr_as_fun(jaxpr)(*loop_idx, *args)
    # Since we're passing in `Ref`s potentially, we need to split out their
    # updated values since we only care about the return values.
    block_indices, _ = split_list(block_indices_and_rest,
                                  [len(self.block_shape)])
    return tuple(i if b is mapped else b * i
                 for b, i in zip(self.block_shape, block_indices))

  replace = dataclasses.replace
