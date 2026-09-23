def has_onnxruntime():
    # FIXME: update test/dynamo/test_backends.py to call is_onnxrt_backend_supported()
    return is_onnxrt_backend_supported()
