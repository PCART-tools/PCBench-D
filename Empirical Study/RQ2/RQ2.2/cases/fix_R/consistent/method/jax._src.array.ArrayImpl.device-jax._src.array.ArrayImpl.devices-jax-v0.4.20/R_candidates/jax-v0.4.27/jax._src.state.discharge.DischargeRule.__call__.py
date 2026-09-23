  def __call__(self, in_avals: Sequence[core.AbstractValue],
      out_avals: Sequence[core.AbstractValue], *args: Any,
      **params: Any) -> tuple[Sequence[Any | None], Sequence[Any]]:
    ...
