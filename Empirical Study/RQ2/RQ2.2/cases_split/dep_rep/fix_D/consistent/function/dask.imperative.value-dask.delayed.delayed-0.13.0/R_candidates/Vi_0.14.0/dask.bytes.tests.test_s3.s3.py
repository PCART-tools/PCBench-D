@pytest.yield_fixture
def s3():
    # writable local S3 system
    with moto.mock_s3():
        client = boto3.client('s3')
        client.create_bucket(Bucket=test_bucket_name, ACL='public-read-write')
        for f, data in files.items():
            client.put_object(Bucket=test_bucket_name, Key=f, Body=data)
        yield S3FileSystem(anon=True)
