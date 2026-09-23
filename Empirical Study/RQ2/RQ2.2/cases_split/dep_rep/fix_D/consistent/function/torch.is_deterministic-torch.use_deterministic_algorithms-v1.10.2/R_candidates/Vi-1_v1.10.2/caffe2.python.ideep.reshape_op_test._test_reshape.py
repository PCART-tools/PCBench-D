def _test_reshape(old_shape, new_shape, expected_shape=None, arg_shape=True,
                  in_place=False, shape_dtype=np.int32):
    devices = [core.DeviceOption(caffe2_pb2.IDEEP, 0)]

    for device_opt in devices:
        with core.DeviceScope(device_opt):
            if expected_shape is None:
                expected_shape = new_shape
            X = np.random.rand(*old_shape).astype(np.float32)

            blob_in = 'X'
            blob_out = blob_in if in_place else blob_in + '_out'

            if arg_shape:
                op = core.CreateOperator('Reshape',
                                         [blob_in],
                                         [blob_out, 'old_shape'],
                                         shape=new_shape)
            else:
                op = core.CreateOperator('Reshape',
                                         [blob_in, 'new_shape'],
                                         [blob_out, 'old_shape'])
                workspace.FeedBlob('new_shape', np.asarray(new_shape, dtype=shape_dtype),
                                   core.DeviceOption(caffe2_pb2.CPU, 0))

            workspace.FeedBlob(blob_in, X)
            workspace.RunOperatorOnce(op)

            Y = workspace.FetchBlob(blob_out)
            np.testing.assert_allclose(Y, X.reshape(expected_shape))
