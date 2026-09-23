  def _get_in_out_specs(self, in_avals, in_tree, out_avals, out_tree):
    if self.in_specs is no_block_spec:
      flat_in_specs = [no_block_spec] * len(in_avals)
    else:
      flat_in_specs = self.in_specs
      if self.in_specs_tree != in_tree:
        raise ValueError(
            "Pytree specs for arguments and `in_specs` must match: "
            f"{in_tree} vs. {self.in_specs_tree}")
    if self.out_specs is no_block_spec:
      flat_out_specs = [no_block_spec] * len(out_avals)
    else:
      flat_out_specs = self.out_specs
      if self.out_specs_tree != out_tree:
        raise ValueError(
            "Pytree specs for `out_shape` and `out_specs` must match: "
            f"{out_tree} vs. {self.out_specs_tree}")
    return flat_in_specs, flat_out_specs
