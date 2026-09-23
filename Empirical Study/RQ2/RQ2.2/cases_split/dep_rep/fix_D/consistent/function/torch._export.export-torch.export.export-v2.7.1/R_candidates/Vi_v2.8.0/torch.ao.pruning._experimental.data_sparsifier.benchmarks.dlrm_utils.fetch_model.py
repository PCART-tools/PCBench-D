def fetch_model(model_path, device, sparse_dlrm=False):
    """This function unzips the zipped model checkpoint (if zipped) and returns a
    model object

    Args:
        model_path (str)
            path pointing to the zipped/raw model checkpoint file that was dumped in evaluate disk savings
        device (torch.device)
            device to which model needs to be loaded to
    """
    if zipfile.is_zipfile(model_path):
        with zipfile.ZipFile(model_path, "r", zipfile.ZIP_DEFLATED) as zip_ref:
            zip_ref.extractall(os.path.dirname(model_path))
            unzip_path = model_path.replace(".zip", ".ckpt")
    else:
        unzip_path = model_path

    model = get_dlrm_model(sparse_dlrm=sparse_dlrm)
    model.load_state_dict(torch.load(unzip_path, map_location=device))
    model = model.to(device)
    model.eval()

    # If there was a zip file, clean up the unzipped files
    if zipfile.is_zipfile(model_path):
        os.remove(unzip_path)

    return model
