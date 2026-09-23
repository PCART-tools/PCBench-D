def allcompare_process(filestore_dir, process_id, data, num_procs):
    from caffe2.python import core, data_parallel_model, workspace, lazy_dyndep
    from caffe2.python.model_helper import ModelHelper
    from caffe2.proto import caffe2_pb2
    lazy_dyndep.RegisterOpsLibrary("@/caffe2/caffe2/distributed:file_store_handler_ops")

    workspace.RunOperatorOnce(
        core.CreateOperator(
            "FileStoreHandlerCreate", [], ["store_handler"], path=filestore_dir
        )
    )
    rendezvous = dict(
        kv_handler="store_handler",
        shard_id=process_id,
        num_shards=num_procs,
        engine=op_engine,
        exit_nets=None
    )

    model = ModelHelper()
    model._rendezvous = rendezvous

    workspace.FeedBlob("test_data", data)

    data_parallel_model._RunComparison(
        model, "test_data", core.DeviceOption(caffe2_pb2.CPU, 0)
    )
