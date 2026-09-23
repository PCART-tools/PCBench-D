def save_any_names_but_these(*names_not_to_save):
  # Save named values, excluding the names given.
  names_not_to_save = frozenset(names_not_to_save)
  def policy(prim, *_, **params):
    if prim is name_p:
      return params['name'] not in names_not_to_save
    return False  # only allow saving named values
  return policy
