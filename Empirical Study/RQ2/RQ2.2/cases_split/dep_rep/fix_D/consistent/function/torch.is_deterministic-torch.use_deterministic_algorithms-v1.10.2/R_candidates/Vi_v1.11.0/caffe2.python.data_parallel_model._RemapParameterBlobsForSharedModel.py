def _RemapParameterBlobsForSharedModel(model, all_params):
    assert model._shared_model
    master_prefix = "{}_{}/".format(
        model._device_prefix, model._devices[0])
    log.info("Remapping param blobs to master -> {}".format(master_prefix))
    master_params = set(model.GetParams())

    # Remove all but master params
    def modify_ops(net):
        ops = []
        for op in net.Proto().op:
            delete_op = False
            # Delete ops that output non-master version of parameter
            for outp in op.output:
                if outp in all_params and outp not in master_params:
                    delete_op = True
                    log.debug("Delete b/c {}:  {}".format(outp, str(op)))
                    break
            if delete_op:
                continue
            # Remap inputs to point to the master param
            for j, inp in enumerate(op.input):
                if inp in all_params and inp not in master_params:
                    op.input[j] = master_prefix + stripBlobName(inp)
            ops.append(op)
        del net.Proto().op[:]
        net.Proto().op.extend(ops)

    modify_ops(model.param_init_net)
    modify_ops(model.net)
