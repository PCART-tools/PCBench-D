from dask.bag.core import from_s3
from moto import mock_s3_deprecated
from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from dask.threaded import get
import inspect
import os

BUCKET = "test-bucket"
KEY = "example.txt"


def main():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"

    with mock_s3_deprecated():
        conn = S3Connection(
            aws_access_key_id="testing",
            aws_secret_access_key="testing",
            is_secure=False,
            calling_format=OrdinaryCallingFormat(),
        )

        bucket = conn.create_bucket(BUCKET)
        key = bucket.new_key(KEY)
        key.set_contents_from_string("line1\nline2\nline3\n")
        bag = from_s3(f"s3://{BUCKET}", KEY, connection=conn)
        print(bag.compute(get=get))

    print("-----getsource_output-----")
    print(inspect.getsource(from_s3))

if __name__ == "__main__":
    main()