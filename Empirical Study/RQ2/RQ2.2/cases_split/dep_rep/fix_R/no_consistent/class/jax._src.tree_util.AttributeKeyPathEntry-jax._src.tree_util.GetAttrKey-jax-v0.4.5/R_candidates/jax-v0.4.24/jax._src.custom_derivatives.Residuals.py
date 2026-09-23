@register_pytree_node_class
class Residuals:
  def __init__(self, jaxpr, in_tree, out_tree, consts):
    self.jaxpr = jaxpr
    self.in_tree = in_tree
    self.out_tree = out_tree
    self.consts = consts
  def __iter__(self):
    return iter((self.jaxpr, self.in_tree, self.out_tree, self.consts))
  def tree_flatten(self):
    return self.consts, (self.jaxpr, self.in_tree, self.out_tree)
  @classmethod
  def tree_unflatten(cls, aux, consts):
    jaxpr, in_tree, out_tree = aux
    return cls(jaxpr, in_tree, out_tree, consts)
