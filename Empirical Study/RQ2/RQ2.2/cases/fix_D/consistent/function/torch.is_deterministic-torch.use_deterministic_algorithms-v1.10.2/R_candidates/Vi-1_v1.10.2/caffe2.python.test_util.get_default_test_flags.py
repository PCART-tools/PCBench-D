def get_default_test_flags():
    return [
        'caffe2',
        '--caffe2_log_level=0',
        '--caffe2_cpu_allocator_do_zero_fill=0',
        '--caffe2_cpu_allocator_do_junk_fill=1',
    ]
