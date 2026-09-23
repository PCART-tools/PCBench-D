def _AnalyzeOperators(model):
    '''
    Look at all the operators and check that they do not cross device scopes
    '''
    for op in model.Proto().op:
        if "NCCL" in op.type or "Copy" in op.type or "Concat" in op.type:
            continue
        if "Sum" == op.type and op.name == "dpm":
            continue
        if "Allreduce" in op.type and "GLOO" in op.engine:
            continue

        op_dev = op.device_option
        op_gpu = op_dev.device_id

        # This avoids failing on operators that are only for CPU
        if not core.IsGPUDeviceType(op_dev.device_type):
            continue

        namescope = "{}_{}/".format(model._device_prefix, op_gpu)
        for inp in list(op.input) + list(op.output):
            if inp.startswith("{}_".format(model._device_prefix)
                             ) and not inp.startswith(namescope):
                raise Exception(
                    "Blob {} of op {}, should have namescope {}. Op: {}".format(
                        inp,
                        op.type,
                        "{}_{}/".format(model._device_prefix, op_gpu),
                        str(op),
                    )
                )
