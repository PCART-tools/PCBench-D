def _AllReduceBlobsDistributed(
    blob_names,
    devices,
    model,
    net,
    rendezvous,
    max_concurrent_distributed_ops,
):
    num_workers = model.net.Proto().num_workers
    assert num_workers > 1, "Please specify more than 1 worker"
    all_reduce_engine = rendezvous['engine']

    master_device_opt = core.DeviceOption(model._device_type, devices[0])

    reducing_device_opt = master_device_opt

    context = CollectivesConcurrencyControl(
        "allreduce",
        max_concurrent_distributed_ops,
        model.param_init_net,
        rendezvous
    )

    nccl_control_blob = None

    for blob_name in blob_names:
        master_blob = model._device_grouped_blobs[blob_name][devices[0]]
        blobs_group = list(viewvalues(model._device_grouped_blobs[blob_name]))

        assert master_blob in blobs_group

        # Remark: NCCLReduce does not support in-place modifications
        # so we need a temporary blob
        reduced_blob = str(master_blob) + "_red"

        def allreduce(blobs, **kwargs):
            with core.DeviceScope(reducing_device_opt):
                comm_world, control_input = \
                    context.get_control_and_context(blobs[0])
                net.Allreduce(
                    inputs=[comm_world] + blobs,
                    outputs=blobs,
                    name=blob_name,
                    engine=all_reduce_engine,
                    control_input=control_input,
                    **kwargs
                )

        if rendezvous['engine'] == 'GLOO':
            # With Gloo cross GPU and cross machine allreduce
            # can be executed in a single operation.
            # Try to use GPUDirect if transport == ibverbs.
            allreduce(
                blobs_group,
                gpu_direct=(rendezvous.get("transport", None) == "ibverbs"),
            )
        else:
            # Step 1: sum blobs from local GPUs to master GPU
            with core.DeviceScope(master_device_opt):
                model.ConstantFill(master_blob, reduced_blob, value=0.0)

                # Temp fix since NCCLReduce does not work
                net.NCCLAllreduce(
                    blobs_group,
                    blobs_group,
                    control_input=nccl_control_blob,
                )
                nccl_control_blob = blobs_group[0]
                net.Copy(master_blob, reduced_blob)

            # Step 2: allreduce between all hosts, between master GPUs
            allreduce([reduced_blob])

            with core.DeviceScope(master_device_opt):
                net.Copy(reduced_blob, master_blob)

            # Step 3: broadcast locally
            _Broadcast(devices, model, net, blob_name)
