def save(name, model, model_jit=None, eg=None, featurestore_meta=None):
    with PackageExporter(str(p / name)) as e:
        e.mock("iopath.**")
        e.intern("**")
        e.save_pickle("model", "model.pkl", model)
        if eg:
            e.save_pickle("model", "example.pkl", eg)
        if featurestore_meta:
            # TODO(whc) can this name come from buck somehow,
            # so it's consistent with predictor_config_constants::METADATA_FILE_NAME()?
            e.save_text("extra_files", "metadata.json", featurestore_meta)

    if model_jit:
        model_jit.save(str(p / (name + "_jit")))
