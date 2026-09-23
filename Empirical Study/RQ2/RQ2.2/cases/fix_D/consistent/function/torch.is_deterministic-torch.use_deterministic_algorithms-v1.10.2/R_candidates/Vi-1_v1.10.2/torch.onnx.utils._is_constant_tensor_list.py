def _is_constant_tensor_list(node):
    if node.kind() != "prim::Constant":
        return False
    output_type = node.output().type()
    if output_type.isSubtypeOf(ListType.ofTensors()):
        return True
    if output_type.isSubtypeOf(ListType(OptionalType.ofTensor())):
        return True
