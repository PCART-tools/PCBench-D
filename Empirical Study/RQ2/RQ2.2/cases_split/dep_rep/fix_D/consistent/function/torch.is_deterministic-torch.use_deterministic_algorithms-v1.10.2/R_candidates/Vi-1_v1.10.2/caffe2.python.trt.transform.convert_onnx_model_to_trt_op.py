def convert_onnx_model_to_trt_op(onnx_model,
        max_batch_size=64,
        max_workspace_size=2*1024*1024,
        verbosity=1,
        debug_builder=False):
    """
    Convert the whole ONNX model to a TensorRT C2 op
    """
    check_gpu_()
    trt_str = C.onnx_to_trt_op(onnx_model.SerializeToString(),
                               _get_output_shapes(onnx_model.graph.output),
                               max_batch_size,
                               max_workspace_size,
                               verbosity,
                               debug_builder)
    op = caffe2_pb2.OperatorDef()
    op.ParseFromString(trt_str)
    return op
