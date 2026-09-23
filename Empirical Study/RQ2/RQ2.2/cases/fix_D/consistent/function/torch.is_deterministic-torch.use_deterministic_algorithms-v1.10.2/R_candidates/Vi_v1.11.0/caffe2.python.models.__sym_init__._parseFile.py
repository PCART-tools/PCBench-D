def _parseFile(filename):
    out_net = caffe2_pb2.NetDef()
    # TODO(bwasti): A more robust handler for pathnames.
    dir_path = os.path.dirname(__file__)
    with open('{dir_path}/{filename}'.format(dir_path=dir_path,
                                             filename=filename), 'rb') as f:
        out_net.ParseFromString(f.read())
    return out_net
