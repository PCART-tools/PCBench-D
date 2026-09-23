def from_s3(bucket_name, paths='*', aws_access_key=None, aws_secret_key=None,
            connection=None, anon=False):
    """ Create a Bag by loading textfiles from s3

    Each line will be treated as one element and each file in S3 as one
    partition.

    You may specify a full s3 bucket

    >>> b = from_s3('s3://bucket-name')  # doctest: +SKIP

    Or select files, lists of files, or globstrings of files within that bucket

    >>> b = from_s3('s3://bucket-name', 'myfile.json')  # doctest: +SKIP
    >>> b = from_s3('s3://bucket-name', ['alice.json', 'bob.json'])  # doctest: +SKIP
    >>> b = from_s3('s3://bucket-name', '*.json')  # doctest: +SKIP
    """
    conn_args = (aws_access_key, aws_secret_key, connection, anon)

    bucket_name, paths = normalize_s3_names(bucket_name, paths, conn_args)

    get_key = partial(_get_key, bucket_name, conn_args)

    name = 'from_s3-' + uuid.uuid4().hex
    dsk = dict(((name, i), (list, (get_key, k))) for i, k in enumerate(paths))
    return Bag(dsk, name, len(paths))
