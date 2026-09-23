def setup_module():
    global old_urlopen

    old_urlopen = urllib_request.urlopen
    urllib_request.urlopen = urlopen_stub
