  def load(self) -> PmapExecutable:
    fingerprint = getattr(self.compiled, "fingerprint", None)

    return PmapExecutable(
        self.compiled, self.build_execute_fun, fingerprint,
        self.local_input_avals, self.jaxpr_debug_info, self)
