@pytest.fixture(scope='module')
def tmpdata(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('tmp')
    tmpdir_path = str(tmpdir.join('mldata'))
    os.makedirs(tmpdir_path)
    yield str(tmpdir)
    shutil.rmtree(str(tmpdir))
