def device_equal(src, dst):
    '''
    We are using this fucntion instead of == operator because optional-value
    comparison between empty device_options and {device_type:0, device_id:0}
    returns not equal in some cases.
    '''
    return src.device_type == dst.device_type and src.device_id == dst.device_id
