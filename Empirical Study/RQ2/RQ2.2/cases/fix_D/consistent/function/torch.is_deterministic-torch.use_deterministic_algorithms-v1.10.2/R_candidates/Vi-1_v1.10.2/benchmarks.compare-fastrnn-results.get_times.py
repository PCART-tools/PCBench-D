def get_times(json_data):
    r = {}
    for fwd_bwd in json_data:
        for test_name in json_data[fwd_bwd]:
            name = construct_name(fwd_bwd, test_name)
            r[name] = json_data[fwd_bwd][test_name]
    return r
