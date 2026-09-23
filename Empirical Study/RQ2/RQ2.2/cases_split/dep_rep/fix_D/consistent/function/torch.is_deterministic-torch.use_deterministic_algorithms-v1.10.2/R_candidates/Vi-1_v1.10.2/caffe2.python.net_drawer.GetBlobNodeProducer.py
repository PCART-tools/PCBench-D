def GetBlobNodeProducer(**kwargs):
    def ReallyGetBlobNode(node_name, label):
        return pydot.Node(node_name, label=label, **kwargs)
    return ReallyGetBlobNode
