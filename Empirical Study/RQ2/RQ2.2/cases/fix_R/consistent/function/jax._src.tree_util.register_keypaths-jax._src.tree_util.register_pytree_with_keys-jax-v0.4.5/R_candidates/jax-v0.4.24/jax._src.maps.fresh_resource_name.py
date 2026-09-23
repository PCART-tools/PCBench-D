def fresh_resource_name(tag=None):
  global _next_resource_id
  try:
    return _UniqueResourceName(_next_resource_id, tag)
  finally:
    _next_resource_id += 1
