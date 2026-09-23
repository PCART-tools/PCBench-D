def gen_covered_ops(source_dir):
    def parse_proto(x):
        proto = caffe2_pb2.OperatorDef()
        proto.ParseFromString(x)
        return proto

    covered = set()
    for f in os.listdir(source_dir):
        zipfile = os.path.join(source_dir, f)
        if not os.path.isfile(zipfile):
            continue
        temp_dir = tempfile.mkdtemp()
        with ZipFile(zipfile) as z:
            z.extractall(temp_dir)
        op_path = os.path.join(temp_dir, 'op.pb')
        with open(op_path, 'rb') as f:
            loaded_op = f.read()
        op_proto = parse_proto(loaded_op)
        covered.add(op_proto.type)

        index = 0
        grad_path = os.path.join(temp_dir, 'grad_{}.pb'.format(index))
        while os.path.isfile(grad_path):
            with open(grad_path, 'rb') as f:
                loaded_grad = f.read()
            grad_proto = parse_proto(loaded_grad)
            covered.add(grad_proto.type)
            index += 1
            grad_path = os.path.join(temp_dir, 'grad_{}.pb'.format(index))
    return covered
