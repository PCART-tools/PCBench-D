def create_node_with_nodes(nodes, name='node'):
    node = hsm_pb2.NodeProto()
    node.name = name
    for child_node in nodes:
        new_child_node = node.children.add()
        new_child_node.MergeFrom(child_node)
    return node
