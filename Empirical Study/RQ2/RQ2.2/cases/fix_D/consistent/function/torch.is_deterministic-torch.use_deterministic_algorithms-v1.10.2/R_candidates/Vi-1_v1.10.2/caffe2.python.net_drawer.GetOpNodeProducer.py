def GetOpNodeProducer(append_output, **kwargs):
    def ReallyGetOpNode(op, op_id):
        if op.name:
            node_name = '%s/%s (op#%d)' % (op.name, op.type, op_id)
        else:
            node_name = '%s (op#%d)' % (op.type, op_id)
        if append_output:
            for output_name in op.output:
                node_name += '\n' + output_name
        return pydot.Node(node_name, **kwargs)
    return ReallyGetOpNode
