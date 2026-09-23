def _hash_bool_list(hash_obj, bool_list):
  for b in bool_list:
    _hash_bool(hash_obj, b)
  _hash_int(hash_obj, len(bool_list))
