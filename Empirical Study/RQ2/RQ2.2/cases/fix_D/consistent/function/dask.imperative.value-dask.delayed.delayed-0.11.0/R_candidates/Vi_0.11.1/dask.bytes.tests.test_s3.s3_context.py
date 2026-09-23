@contextmanager
def s3_context(bucket, files):
    m = moto.mock_s3()
    m.start()
    client = boto3.client('s3')
    client.create_bucket(Bucket=bucket, ACL='public-read-write')
    for f, data in files.items():
        client.put_object(Bucket=bucket, Key=f, Body=data)

    yield S3FileSystem(anon=True)

    for f, data in files.items():
        try:
            client.delete_object(Bucket=bucket, Key=f, Body=data)
        except:
            pass
    m.stop()
