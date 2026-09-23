@click.command(
    help='convert onnx model to caffe2 net',
    context_settings={
        'help_option_names': ['-h', '--help']
    }
)
@click.argument('onnx_model', type=click.File('rb'))
@click.option('-o', '--output', required=True,
              type=click.File('wb'),
              help='Output path for the caffe2 net file')
@click.option('--init-net-output',
              required=True,
              type=click.File('wb'),
              help='Output path for the caffe2 init net file')
def onnx_to_caffe2(onnx_model, output, init_net_output):
    onnx_model_proto = ModelProto()
    onnx_model_proto.ParseFromString(onnx_model.read())

    init_net, predict_net = c2.onnx_graph_to_caffe2_net(onnx_model_proto)
    init_net_output.write(init_net.SerializeToString())
    output.write(predict_net.SerializeToString())
