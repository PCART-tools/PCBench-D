def setUpModule():
    # Do nothing if caffe and test data is not found
    if not (CAFFE_FOUND and os.path.exists('data/testdata/caffe_translator')):
        return
    # We will do all the computation stuff in the global space.
    caffenet = caffe_pb2.NetParameter()
    caffenet_pretrained = caffe_pb2.NetParameter()
    with open('data/testdata/caffe_translator/deploy.prototxt') as f:
        text_format.Merge(f.read(), caffenet)
    with open('data/testdata/caffe_translator/'
              'bvlc_reference_caffenet.caffemodel') as f:
        caffenet_pretrained.ParseFromString(f.read())
    for remove_legacy_pad in [True, False]:
        net, pretrained_params = caffe_translator.TranslateModel(
            caffenet, caffenet_pretrained, is_test=True,
            remove_legacy_pad=remove_legacy_pad
        )
        with open('data/testdata/caffe_translator/'
                  'bvlc_reference_caffenet.translatedmodel',
                  'w') as fid:
            fid.write(str(net))
        for param in pretrained_params.protos:
            workspace.FeedBlob(param.name, utils.Caffe2TensorToNumpyArray(param))
        # Let's also feed in the data from the Caffe test code.
        data = np.load('data/testdata/caffe_translator/data_dump.npy').astype(
            np.float32)
        workspace.FeedBlob('data', data)
        # Actually running the test.
        workspace.RunNetOnce(net.SerializeToString())
