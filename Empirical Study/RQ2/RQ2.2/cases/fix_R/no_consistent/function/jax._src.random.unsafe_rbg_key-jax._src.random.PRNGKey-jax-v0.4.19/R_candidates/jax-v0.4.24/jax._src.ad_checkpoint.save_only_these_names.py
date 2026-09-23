def save_only_these_names(*names_which_can_be_saved):
  """Save only named values, and only among the names given."""
  names_which_can_be_saved = set(names_which_can_be_saved)
  def policy(prim, *_, **params):
    if prim is name_p:
      return params['name'] in names_which_can_be_saved
    return False  # not saveable unless it's in the allow-list
  return policy
