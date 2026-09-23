def setup(path):
    sys.path.extend(python_path(path))
    sys.path.append('build/lib')  # for our test python extension
