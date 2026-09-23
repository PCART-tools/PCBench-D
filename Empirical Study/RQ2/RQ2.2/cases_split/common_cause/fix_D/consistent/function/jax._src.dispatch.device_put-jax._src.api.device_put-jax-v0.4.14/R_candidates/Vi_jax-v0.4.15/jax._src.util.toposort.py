def toposort(end_nodes):
  if not end_nodes: return []
  end_nodes = _remove_duplicates(end_nodes)

  child_counts = {}
  stack = list(end_nodes)
  while stack:
    node = stack.pop()
    if id(node) in child_counts:
      child_counts[id(node)] += 1
    else:
      child_counts[id(node)] = 1
      stack.extend(node.parents)
  for node in end_nodes:
    child_counts[id(node)] -= 1

  sorted_nodes = []
  childless_nodes = [node for node in end_nodes if child_counts[id(node)] == 0]
  assert childless_nodes
  while childless_nodes:
    node = childless_nodes.pop()
    sorted_nodes.append(node)
    for parent in node.parents:
      if child_counts[id(parent)] == 1:
        childless_nodes.append(parent)
      else:
        child_counts[id(parent)] -= 1
  sorted_nodes = sorted_nodes[::-1]

  check_toposort(sorted_nodes)
  return sorted_nodes
