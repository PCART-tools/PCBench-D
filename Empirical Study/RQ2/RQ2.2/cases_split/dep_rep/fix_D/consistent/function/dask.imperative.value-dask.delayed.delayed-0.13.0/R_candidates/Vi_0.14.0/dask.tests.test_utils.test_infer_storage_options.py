def test_infer_storage_options():
    so = infer_storage_options('/mnt/datasets/test.csv')
    assert so.pop('protocol') == 'file'
    assert so.pop('path') == '/mnt/datasets/test.csv'
    assert not so

    assert infer_storage_options('./test.csv')['path'] == './test.csv'
    assert infer_storage_options('../test.csv')['path'] == '../test.csv'

    so = infer_storage_options('C:\\test.csv')
    assert so.pop('protocol') == 'file'
    assert so.pop('path') == 'C:\\test.csv'
    assert not so

    assert infer_storage_options('d:\\test.csv')['path'] == 'd:\\test.csv'
    assert infer_storage_options('\\test.csv')['path'] == '\\test.csv'
    assert infer_storage_options('.\\test.csv')['path'] == '.\\test.csv'
    assert infer_storage_options('test.csv')['path'] == 'test.csv'

    so = infer_storage_options(
        'hdfs://username:pwd@Node:123/mnt/datasets/test.csv?q=1#fragm',
        inherit_storage_options={'extra': 'value'})
    assert so.pop('protocol') == 'hdfs'
    assert so.pop('username') == 'username'
    assert so.pop('password') == 'pwd'
    assert so.pop('host') == 'Node'
    assert so.pop('port') == 123
    assert so.pop('path') == '/mnt/datasets/test.csv'
    assert so.pop('url_query') == 'q=1'
    assert so.pop('url_fragment') == 'fragm'
    assert so.pop('extra') == 'value'
    assert not so

    so = infer_storage_options('hdfs://User-name@Node-name.com/mnt/datasets/test.csv')
    assert so.pop('username') == 'User-name'
    assert so.pop('host') == 'Node-name.com'

    assert infer_storage_options('s3://Bucket-name.com/test.csv')['host'] == 'Bucket-name.com'
    assert infer_storage_options('http://127.0.0.1:8080/test.csv')['host'] == '127.0.0.1'

    with pytest.raises(KeyError):
        infer_storage_options('file:///bucket/file.csv', {'path': 'collide'})
    with pytest.raises(KeyError):
        infer_storage_options('hdfs:///bucket/file.csv', {'protocol': 'collide'})
