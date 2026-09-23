def setThrowIfFpExceptions(enabled):
    core.GlobalInit(["caffe2", "--caffe2_operator_throw_if_fp_exceptions=%d" % (1 if enabled else 0)])
