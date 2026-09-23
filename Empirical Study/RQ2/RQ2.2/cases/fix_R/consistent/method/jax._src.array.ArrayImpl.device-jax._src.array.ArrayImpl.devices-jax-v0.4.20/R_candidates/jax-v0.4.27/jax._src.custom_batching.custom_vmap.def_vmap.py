  def def_vmap(self, vmap_rule: Callable) -> Callable:
    self.vmap_rule = vmap_rule
    return vmap_rule
