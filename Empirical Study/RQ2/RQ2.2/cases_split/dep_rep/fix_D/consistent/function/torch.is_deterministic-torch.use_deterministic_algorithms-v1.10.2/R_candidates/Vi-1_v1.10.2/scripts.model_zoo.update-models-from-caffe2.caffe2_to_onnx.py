def caffe2_to_onnx(caffe2_model_name, caffe2_model_dir):
    caffe2_init_proto = caffe2_pb2.NetDef()
    caffe2_predict_proto = caffe2_pb2.NetDef()

    with open(os.path.join(caffe2_model_dir, 'init_net.pb'), 'rb') as f:
        caffe2_init_proto.ParseFromString(f.read())
        caffe2_init_proto.name = '{}_init'.format(caffe2_model_name)
    with open(os.path.join(caffe2_model_dir, 'predict_net.pb'), 'rb') as f:
        caffe2_predict_proto.ParseFromString(f.read())
        caffe2_predict_proto.name = caffe2_model_name
    with open(os.path.join(caffe2_model_dir, 'value_info.json'), 'rb') as f:
        value_info = json.loads(f.read())

    print('Converting Caffe2 model {} in {} to ONNX format'.format(caffe2_model_name, caffe2_model_dir))
    onnx_model = caffe2.python.onnx.frontend.caffe2_net_to_onnx_model(
        init_net=caffe2_init_proto,
        predict_net=caffe2_predict_proto,
        value_info=value_info
    )

    return onnx_model, caffe2_init_proto, caffe2_predict_proto
