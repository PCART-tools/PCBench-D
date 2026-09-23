def _hash_signed_int(hash_obj, int_var):
  hash_obj.update(int_var.to_bytes(8, byteorder="big", signed=True))
