def test_pickability_of_lazy_files(tmpdir):
    cloudpickle = pytest.importorskip('cloudpickle')
    fn = os.path.join(str(tmpdir), 'foo')
    with open(fn, 'wb') as f:
        f.write(b'1')

    opener = OpenFileCreator('file://foo.py', open=open)
    opener2 = cloudpickle.loads(cloudpickle.dumps(opener))
    assert type(opener2.fs) == type(opener.fs)

    lazy_file = opener(fn, mode='rt')
    lazy_file2 = cloudpickle.loads(cloudpickle.dumps(lazy_file))
    assert lazy_file.path == lazy_file2.path

    with lazy_file as f:
        pass

    lazy_file3 = cloudpickle.loads(cloudpickle.dumps(lazy_file))
    assert lazy_file.path == lazy_file3.path
