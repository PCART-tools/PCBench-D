  def __init__(self, shardings: tuple[GSPMDSharding | UnspecifiedValue, ...],
               avals: tuple[core.AbstractValue]):
    if xla_extension_version < 241:
      gspmd_shardings = [
          s if is_unspecified_or_auto(s) or a is core.abstract_token
          else to_gspmd_sharding(s, a.ndim)  # type: ignore
          for s, a in zip(shardings, avals)]
    else:
      gspmd_shardings = [
          s if is_unspecified_or_auto(s) else to_gspmd_sharding(s, a.ndim)  # type: ignore
          for s, a in zip(shardings, avals)]
    self._gspmd_shardings = gspmd_shardings
    self.shardings = shardings
    self.avals = avals
