def save_anything_except_these_names(*names_not_to_save):
  """Save any values (not just named ones) excluding the names given."""
  names_not_to_save = frozenset(names_not_to_save)
  def policy(prim, *_, **params):
    if prim is name_p:
      return params['name'] not in names_not_to_save
    return True  # allow saving anything which is not named
  return policy
