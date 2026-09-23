def check_toposort(nodes):
  visited = set()
  for node in nodes:
    assert all(id(parent) in visited for parent in node.parents)
    visited.add(id(node))
