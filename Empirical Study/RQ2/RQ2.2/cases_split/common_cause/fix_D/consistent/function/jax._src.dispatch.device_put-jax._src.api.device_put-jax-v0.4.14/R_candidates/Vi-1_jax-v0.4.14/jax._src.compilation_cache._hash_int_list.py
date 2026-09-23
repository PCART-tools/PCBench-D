def _hash_int_list(hash_obj, int_list):
  for i in int_list:
    _hash_int(hash_obj, i)
  _hash_int(hash_obj, len(int_list))
