def _download_onnx_model(model_name, opset_version):
    onnx_home = os.path.expanduser(os.getenv('ONNX_HOME', os.path.join('~', '.onnx')))
    models_dir = os.getenv('ONNX_MODELS',
                           os.path.join(onnx_home, 'models'))
    model_dir = os.path.join(models_dir, model_name)
    if not os.path.exists(os.path.join(model_dir, 'model.onnx')):
        if os.path.exists(model_dir):
            bi = 0
            while True:
                dest = '{}.old.{}'.format(model_dir, bi)
                if os.path.exists(dest):
                    bi += 1
                    continue
                shutil.move(model_dir, dest)
                break
        os.makedirs(model_dir)

        # On Windows, NamedTemporaryFile can not be opened for a
        # second time
        url = '{}/{}.tar.gz'.format(_base_url(opset_version), model_name)
        download_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            download_file.close()
            print('Start downloading model {} from {}'.format(
                model_name, url))
            urlretrieve(url, download_file.name)
            print('Done')
            with tarfile.open(download_file.name) as t:
                t.extractall(models_dir)
        except Exception as e:
            print('Failed to prepare data for model {}: {}'.format(
                model_name, e))
            raise
        finally:
            os.remove(download_file.name)
    return model_dir
