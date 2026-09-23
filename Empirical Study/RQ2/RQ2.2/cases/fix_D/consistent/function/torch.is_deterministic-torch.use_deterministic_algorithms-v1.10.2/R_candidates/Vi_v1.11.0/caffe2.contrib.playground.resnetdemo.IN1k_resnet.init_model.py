def init_model(self):
    train_model = cnn.CNNModelHelper(
        order="NCHW",
        name="resnet",
        use_cudnn=True,
        cudnn_exhaustive_search=False
    )
    self.train_model = train_model

    test_model = cnn.CNNModelHelper(
        order="NCHW",
        name="resnet_test",
        use_cudnn=True,
        cudnn_exhaustive_search=False,
        init_params=False,
    )
    self.test_model = test_model

    self.log.info("Model creation completed")
