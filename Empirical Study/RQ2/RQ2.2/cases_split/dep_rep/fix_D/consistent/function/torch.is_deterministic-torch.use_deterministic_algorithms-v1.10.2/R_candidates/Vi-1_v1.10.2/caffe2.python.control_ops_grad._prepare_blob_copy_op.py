def _prepare_blob_copy_op(from_name, to_name):
    copy_op_def = caffe2_pb2.OperatorDef()
    copy_op_def.type = "Copy"
    copy_op_def.input.extend([from_name])
    copy_op_def.output.extend([to_name])
    return copy_op_def
