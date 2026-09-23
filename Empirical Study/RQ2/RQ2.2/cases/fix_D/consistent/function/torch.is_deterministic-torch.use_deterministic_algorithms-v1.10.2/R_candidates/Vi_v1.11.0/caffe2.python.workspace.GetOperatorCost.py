def GetOperatorCost(operator, blobs):
    return C.get_operator_cost(StringifyProto(operator), blobs)
