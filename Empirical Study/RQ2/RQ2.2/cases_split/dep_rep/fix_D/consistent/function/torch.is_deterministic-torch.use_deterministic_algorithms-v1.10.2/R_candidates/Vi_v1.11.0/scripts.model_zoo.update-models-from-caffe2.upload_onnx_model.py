def upload_onnx_model(model_name, zoo_dir, backup=False, only_local=False):
    if only_local:
        print('No uploading in local only mode.')
        return
    model_dir = os.path.join(zoo_dir, model_name)
    suffix = '-backup' if backup else ''
    if backup:
        print('Backing up the previous version of ONNX model {}...'.format(model_name))
    rel_file_name = '{}{}.tar.gz'.format(model_name, suffix)
    abs_file_name = os.path.join(zoo_dir, rel_file_name)
    print('Compressing {} model to {}'.format(model_name, abs_file_name))
    with tarfile.open(abs_file_name, 'w:gz') as f:
        f.add(model_dir, arcname=model_name)
    file_size = os.stat(abs_file_name).st_size
    print('Uploading {} ({} MB) to s3 cloud...'.format(abs_file_name, float(file_size) / 1024 / 1024))
    client = boto3.client('s3', 'us-east-1')
    transfer = boto3.s3.transfer.S3Transfer(client)
    transfer.upload_file(abs_file_name, 'download.onnx', 'models/latest/{}'.format(rel_file_name),
                         extra_args={'ACL': 'public-read'})

    print('Successfully uploaded {} to s3!'.format(rel_file_name))
