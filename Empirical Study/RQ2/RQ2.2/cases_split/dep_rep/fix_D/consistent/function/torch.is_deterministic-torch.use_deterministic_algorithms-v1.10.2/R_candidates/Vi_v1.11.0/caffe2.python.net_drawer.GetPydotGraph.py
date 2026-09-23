def GetPydotGraph(
    operators_or_net,
    name=None,
    rankdir='LR',
    op_node_producer=None,
    blob_node_producer=None
):
    if op_node_producer is None:
        op_node_producer = GetOpNodeProducer(False, **OP_STYLE)
    if blob_node_producer is None:
        blob_node_producer = GetBlobNodeProducer(**BLOB_STYLE)
    operators, name = _rectify_operator_and_name(operators_or_net, name)
    graph = pydot.Dot(name, rankdir=rankdir)
    pydot_nodes = {}
    pydot_node_counts = defaultdict(int)
    for op_id, op in enumerate(operators):
        op_node = op_node_producer(op, op_id)
        graph.add_node(op_node)
        # print 'Op: %s' % op.name
        # print 'inputs: %s' % str(op.input)
        # print 'outputs: %s' % str(op.output)
        for input_name in op.input:
            if input_name not in pydot_nodes:
                input_node = blob_node_producer(
                    _escape_label(
                        input_name + str(pydot_node_counts[input_name])),
                    label=_escape_label(input_name),
                )
                pydot_nodes[input_name] = input_node
            else:
                input_node = pydot_nodes[input_name]
            graph.add_node(input_node)
            graph.add_edge(pydot.Edge(input_node, op_node))
        for output_name in op.output:
            if output_name in pydot_nodes:
                # we are overwriting an existing blob. need to update the count.
                pydot_node_counts[output_name] += 1
            output_node = blob_node_producer(
                _escape_label(
                    output_name + str(pydot_node_counts[output_name])),
                label=_escape_label(output_name),
            )
            pydot_nodes[output_name] = output_node
            graph.add_node(output_node)
            graph.add_edge(pydot.Edge(op_node, output_node))
    return graph
