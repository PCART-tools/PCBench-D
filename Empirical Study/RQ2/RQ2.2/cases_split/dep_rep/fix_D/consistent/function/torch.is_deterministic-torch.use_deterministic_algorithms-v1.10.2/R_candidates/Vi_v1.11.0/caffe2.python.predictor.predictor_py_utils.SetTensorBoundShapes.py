def SetTensorBoundShapes(meta_net_def, tensor_bound_shapes):
    meta_net_def.tensorBoundShapes.CopyFrom(tensor_bound_shapes)
