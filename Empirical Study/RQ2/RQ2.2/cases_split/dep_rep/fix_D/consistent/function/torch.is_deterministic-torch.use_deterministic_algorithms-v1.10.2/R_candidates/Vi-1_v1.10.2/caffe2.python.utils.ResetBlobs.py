def ResetBlobs(blobs):
    from caffe2.python import workspace, core
    workspace.RunOperatorOnce(
        core.CreateOperator(
            "Free",
            list(blobs),
            list(blobs),
            device_option=core.DeviceOption(caffe2_pb2.CPU),
        ),
    )
