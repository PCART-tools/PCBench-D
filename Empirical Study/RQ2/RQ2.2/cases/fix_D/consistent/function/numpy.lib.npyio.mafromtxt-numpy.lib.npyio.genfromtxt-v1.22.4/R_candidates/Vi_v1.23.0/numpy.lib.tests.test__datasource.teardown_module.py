def teardown_module():
    urllib_request.urlopen = old_urlopen
