def GetGraphInJson(operators_or_net, output_filepath):
    operators, _ = _rectify_operator_and_name(operators_or_net, None)
    blob_strid_to_node_id = {}
    node_name_counts = defaultdict(int)
    nodes = []
    edges = []
    for op_id, op in enumerate(operators):
        op_label = op.name + '/' + op.type if op.name else op.type
        op_node_id = len(nodes)
        nodes.append({
            'id': op_node_id,
            'label': op_label,
            'op_id': op_id,
            'type': 'op'
        })
        for input_name in op.input:
            strid = _escape_label(
                input_name + str(node_name_counts[input_name]))
            if strid not in blob_strid_to_node_id:
                input_node = {
                    'id': len(nodes),
                    'label': input_name,
                    'type': 'blob'
                }
                blob_strid_to_node_id[strid] = len(nodes)
                nodes.append(input_node)
            else:
                input_node = nodes[blob_strid_to_node_id[strid]]
            edges.append({
                'source': blob_strid_to_node_id[strid],
                'target': op_node_id
            })
        for output_name in op.output:
            strid = _escape_label(
                output_name + str(node_name_counts[output_name]))
            if strid in blob_strid_to_node_id:
                # we are overwriting an existing blob. need to update the count.
                node_name_counts[output_name] += 1
                strid = _escape_label(
                    output_name + str(node_name_counts[output_name]))

            if strid not in blob_strid_to_node_id:
                output_node = {
                    'id': len(nodes),
                    'label': output_name,
                    'type': 'blob'
                }
                blob_strid_to_node_id[strid] = len(nodes)
                nodes.append(output_node)
            edges.append({
                'source': op_node_id,
                'target': blob_strid_to_node_id[strid]
            })

    with open(output_filepath, 'w') as f:
        json.dump({'nodes': nodes, 'edges': edges}, f)
