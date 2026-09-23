def download_onnx_model(model_name, zoo_dir, use_cache=True, only_local=False):
    model_dir = os.path.join(zoo_dir, model_name)
    if os.path.exists(model_dir):
        if use_cache:
            upload_onnx_model(model_name, zoo_dir, backup=True, only_local=only_local)
            return
        else:
            shutil.rmtree(model_dir)
    url = 'https://s3.amazonaws.com/download.onnx/models/latest/{}.tar.gz'.format(model_name)

    download_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        download_file.close()
        print('Downloading ONNX model {} from {} and save in {} ...\n'.format(
            model_name, url, download_file.name))
        urlretrieve(url, download_file.name)
        with tarfile.open(download_file.name) as t:
            print('Extracting ONNX model {} to {} ...\n'.format(model_name, zoo_dir))
            t.extractall(zoo_dir)
    except Exception as e:
        print('Failed to download/backup data for ONNX model {}: {}'.format(model_name, e))
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
    finally:
        os.remove(download_file.name)

    if not only_local:
        upload_onnx_model(model_name, zoo_dir, backup=True, only_local=only_local)
