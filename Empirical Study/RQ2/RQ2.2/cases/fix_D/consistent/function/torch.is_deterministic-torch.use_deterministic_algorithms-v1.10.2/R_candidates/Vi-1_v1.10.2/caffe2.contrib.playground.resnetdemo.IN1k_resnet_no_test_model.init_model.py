def init_model(self):
    # if cudnn needs to be turned off, several other places
    # need to be modified:
    # 1. operators need to be constructed with engine option, like below:
    #     conv_blob = model.Conv(...engine=engine)
    # 2. when launch model, opts['model_param']['engine'] = "" instead of "CUDNN"
    # 2. caffe2_disable_implicit_engine_preference in operator.cc set to true
    train_model = cnn.CNNModelHelper(
        order="NCHW",
        name="resnet",
        use_cudnn=False,
        cudnn_exhaustive_search=False,
    )
    self.train_model = train_model

    # test_model = cnn.CNNModelHelper(
    #     order="NCHW",
    #     name="resnet_test",
    #     use_cudnn=False,
    #     cudnn_exhaustive_search=False,
    #     init_params=False,
    # )
    self.test_model = None

    self.log.info("Model creation completed")
