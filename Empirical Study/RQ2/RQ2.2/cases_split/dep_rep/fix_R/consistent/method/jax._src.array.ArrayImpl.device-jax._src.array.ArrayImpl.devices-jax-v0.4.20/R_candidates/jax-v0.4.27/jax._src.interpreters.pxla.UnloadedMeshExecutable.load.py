  def load(self) -> MeshExecutable:
    return MeshExecutable(self.xla_executable, self.build_unsafe_call,
                          self.input_avals, self.output_avals,
                          self.input_shardings, self.output_shardings,
                          self.auto_spmd_lowering, self.kept_var_idx,
                          self.in_layouts, self.out_layouts,
                          self.all_args_info, self)
