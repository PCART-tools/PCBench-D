def download_caffe2_model(model_name, zoo_dir, use_cache=True):
    model_dir = os.path.join(zoo_dir, model_name)
    if os.path.exists(model_dir):
        if use_cache:
            return
        else:
            shutil.rmtree(model_dir)
    os.makedirs(model_dir)

    for f in ['predict_net.pb', 'init_net.pb', 'value_info.json']:
        url = getURLFromName(model_name, f)
        dest = os.path.join(model_dir, f)
        try:
            try:
                downloadFromURLToFile(url, dest,
                                      show_progress=False)
            except TypeError:
                # show_progress not supported prior to
                # Caffe2 78c014e752a374d905ecfb465d44fa16e02a28f1
                # (Sep 17, 2017)
                downloadFromURLToFile(url, dest)
        except Exception as e:
            print("Abort: {reason}".format(reason=e))
            print("Cleaning up...")
            deleteDirectory(model_dir)
            raise
