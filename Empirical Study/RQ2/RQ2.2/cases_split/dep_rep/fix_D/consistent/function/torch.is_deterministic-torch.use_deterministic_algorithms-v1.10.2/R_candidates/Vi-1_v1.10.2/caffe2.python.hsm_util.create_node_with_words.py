def create_node_with_words(words, name='node'):
    node = hsm_pb2.NodeProto()
    node.name = name
    for word in words:
        node.word_ids.append(word)
    return node
