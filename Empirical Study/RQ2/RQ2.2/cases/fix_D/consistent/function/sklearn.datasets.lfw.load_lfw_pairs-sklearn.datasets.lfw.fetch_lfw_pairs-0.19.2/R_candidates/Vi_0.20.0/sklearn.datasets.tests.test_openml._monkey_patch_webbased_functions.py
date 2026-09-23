def _monkey_patch_webbased_functions(context,
                                     data_id,
                                     gzip_response):
    url_prefix_data_description = "https://openml.org/api/v1/json/data/"
    url_prefix_data_features = "https://openml.org/api/v1/json/data/features/"
    url_prefix_download_data = "https://openml.org/data/v1/"
    url_prefix_data_list = "https://openml.org/api/v1/json/data/list/"

    path_suffix = '.gz'
    read_fn = gzip.open

    class MockHTTPResponse(object):
        def __init__(self, data, is_gzip):
            self.data = data
            self.is_gzip = is_gzip

        def read(self, amt=-1):
            return self.data.read(amt)

        def tell(self):
            return self.data.tell()

        def seek(self, pos, whence=0):
            return self.data.seek(pos, whence)

        def close(self):
            self.data.close()

        def info(self):
            if self.is_gzip:
                return {'Content-Encoding': 'gzip'}
            return {}

    def _file_name(url, suffix):
        return (re.sub(r'\W', '-', url[len("https://openml.org/"):])
                + suffix + path_suffix)

    def _mock_urlopen_data_description(url, has_gzip_header):
        assert url.startswith(url_prefix_data_description)

        path = os.path.join(currdir, 'data', 'openml', str(data_id),
                            _file_name(url, '.json'))

        if has_gzip_header and gzip_response:
            fp = open(path, 'rb')
            return MockHTTPResponse(fp, True)
        else:
            fp = read_fn(path, 'rb')
            return MockHTTPResponse(fp, False)

    def _mock_urlopen_data_features(url, has_gzip_header):
        assert url.startswith(url_prefix_data_features)
        path = os.path.join(currdir, 'data', 'openml', str(data_id),
                            _file_name(url, '.json'))
        if has_gzip_header and gzip_response:
            fp = open(path, 'rb')
            return MockHTTPResponse(fp, True)
        else:
            fp = read_fn(path, 'rb')
            return MockHTTPResponse(fp, False)

    def _mock_urlopen_download_data(url, has_gzip_header):
        assert (url.startswith(url_prefix_download_data))

        path = os.path.join(currdir, 'data', 'openml', str(data_id),
                            _file_name(url, '.arff'))

        if has_gzip_header and gzip_response:
            fp = open(path, 'rb')
            return MockHTTPResponse(fp, True)
        else:
            fp = read_fn(path, 'rb')
            return MockHTTPResponse(fp, False)

    def _mock_urlopen_data_list(url, has_gzip_header):
        assert url.startswith(url_prefix_data_list)

        json_file_path = os.path.join(currdir, 'data', 'openml',
                                      str(data_id), _file_name(url, '.json'))
        # load the file itself, to simulate a http error
        json_data = json.loads(read_fn(json_file_path, 'rb').
                               read().decode('utf-8'))
        if 'error' in json_data:
            raise HTTPError(url=None, code=412,
                            msg='Simulated mock error',
                            hdrs=None, fp=None)

        if has_gzip_header:
            fp = open(json_file_path, 'rb')
            return MockHTTPResponse(fp, True)
        else:
            fp = read_fn(json_file_path, 'rb')
            return MockHTTPResponse(fp, False)

    def _mock_urlopen(request):
        url = request.get_full_url()
        has_gzip_header = request.get_header('Accept-encoding') == "gzip"
        if url.startswith(url_prefix_data_list):
            return _mock_urlopen_data_list(url, has_gzip_header)
        elif url.startswith(url_prefix_data_features):
            return _mock_urlopen_data_features(url, has_gzip_header)
        elif url.startswith(url_prefix_download_data):
            return _mock_urlopen_download_data(url, has_gzip_header)
        elif url.startswith(url_prefix_data_description):
            return _mock_urlopen_data_description(url, has_gzip_header)
        else:
            raise ValueError('Unknown mocking URL pattern: %s' % url)

    # XXX: Global variable
    if test_offline:
        context.setattr(sklearn.datasets.openml, 'urlopen', _mock_urlopen)
