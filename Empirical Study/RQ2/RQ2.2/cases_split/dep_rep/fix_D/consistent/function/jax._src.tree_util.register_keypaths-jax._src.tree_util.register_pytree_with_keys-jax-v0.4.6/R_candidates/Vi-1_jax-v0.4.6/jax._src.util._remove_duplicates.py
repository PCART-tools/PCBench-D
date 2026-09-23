def _remove_duplicates(node_list):
  seen = set()
  out = []
  for n in node_list:
    if id(n) not in seen:
      seen.add(id(n))
      out.append(n)
  return out
