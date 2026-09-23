class JaxprPpContext:
  var_names: defaultdict[Var, str]
  used_names: MutableSet[str]
  top_level_jaxprs: MutableMapping[Jaxpr, str]

  def __init__(self) -> None:
    self.top_level_jaxprs = {}
    self.used_names = set()
    fresh_names: Iterator[str] = (
        name
        for i in it.count()
        if (name := _encode_digits_alphabetic(i)) not in self.used_names
    )
    self.var_names = defaultdict(fresh_names.__next__)
