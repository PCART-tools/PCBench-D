  def cost_analysis(self) -> dict[str, float]:
    backend = self.compile_args["backend"]
    if xb.using_pjrt_c_api(backend):
      raise NotImplementedError(
          "Lowered.cost_analysis not implemented on platform "
          f"'{backend.platform}'. Use compile().cost_analysis() for "  # type: ignore
          "post-compilation cost estimates.")
    return xe.hlo_module_cost_analysis(backend, self.hlo().as_hlo_module())
