def SaveModel(args, train_model, epoch, use_ideep):
    prefix = "[]_{}".format(train_model._device_prefix, train_model._devices[0])
    predictor_export_meta = pred_exp.PredictorExportMeta(
        predict_net=train_model.net.Proto(),
        parameters=data_parallel_model.GetCheckpointParams(train_model),
        inputs=[prefix + "/data"],
        outputs=[prefix + "/softmax"],
        shapes={
            prefix + "/softmax": (1, args.num_labels),
            prefix + "/data": (args.num_channels, args.image_size, args.image_size)
        }
    )

    # save the train_model for the current epoch
    model_path = "%s/%s_%d.mdl" % (
        args.file_store_path,
        args.save_model_name,
        epoch,
    )

    # set db_type to be "minidb" instead of "log_file_db", which breaks
    # the serialization in save_to_db. Need to switch back to log_file_db
    # after migration
    pred_exp.save_to_db(
        db_type="minidb",
        db_destination=model_path,
        predictor_export_meta=predictor_export_meta,
        use_ideep=use_ideep
    )
