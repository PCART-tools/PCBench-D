def gen_init_net_from_blobs(blobs):
    ''' Generate an initialization net based on a blob dict '''
    ret = caffe2_pb2.NetDef()
    for name, blob in blobs.items():
        add_tensor(ret, name, blob)
    return ret
