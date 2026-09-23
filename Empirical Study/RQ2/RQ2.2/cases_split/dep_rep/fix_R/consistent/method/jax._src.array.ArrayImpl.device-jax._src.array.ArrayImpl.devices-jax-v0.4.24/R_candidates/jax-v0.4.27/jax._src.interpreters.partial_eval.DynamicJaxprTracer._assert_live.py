  def _assert_live(self) -> None:
    if not self._trace.main.jaxpr_stack:  # type: ignore
      raise core.escaped_tracer_error(self, None)
