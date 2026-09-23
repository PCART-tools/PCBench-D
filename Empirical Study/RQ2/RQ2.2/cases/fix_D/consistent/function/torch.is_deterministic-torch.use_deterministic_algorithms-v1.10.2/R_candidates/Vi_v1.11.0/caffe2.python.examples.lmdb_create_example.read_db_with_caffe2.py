def read_db_with_caffe2(db_file, expected_checksum):
    print(">>> Read database...")
    model = model_helper.ModelHelper(name="lmdbtest")
    batch_size = 32
    data, label = model.TensorProtosDBInput(
        [], ["data", "label"], batch_size=batch_size,
        db=db_file, db_type="lmdb")

    checksum = 0

    workspace.RunNetOnce(model.param_init_net)
    workspace.CreateNet(model.net)

    for _ in range(0, 4):
        workspace.RunNet(model.net.Proto().name)

        img_datas = workspace.FetchBlob("data")
        labels = workspace.FetchBlob("label")
        for j in range(batch_size):
            checksum += np.sum(img_datas[j, :]) * labels[j]

    print("Checksum/read: {}".format(int(checksum)))
    assert np.abs(expected_checksum - checksum < 0.1), \
        "Read/write checksums dont match"
