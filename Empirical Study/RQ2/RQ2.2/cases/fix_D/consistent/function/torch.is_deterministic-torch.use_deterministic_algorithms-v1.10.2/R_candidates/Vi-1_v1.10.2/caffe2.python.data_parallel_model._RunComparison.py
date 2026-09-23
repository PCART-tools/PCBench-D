def _RunComparison(model, blob_name, device=None):
    if device is None:
        device = model._blob_to_device[blob_name]
    with core.DeviceScope(device):
        rendezvous = model._rendezvous
        if rendezvous is None or rendezvous['num_shards'] == 1:
            return True

        test_data_arr = np.zeros(rendezvous['num_shards']).astype(np.float32)
        test_data_arr[rendezvous['shard_id']] = 1
        workspace.FeedBlob("compare_arr", test_data_arr)

        comparison_net = core.Net("allcompare_net")

        kwargs=dict()
        if 'mpi_rendezvous' in rendezvous:
            kwargs['mpi_rendezvous'] = rendezvous['mpi_rendezvous']
        comm_world = comparison_net.CreateCommonWorld(
            rendezvous['kv_handler'] or [],
            "initial_sync",
            name=model.net.Proto().name + ".cw_master_select",
            size=rendezvous['num_shards'],
            rank=rendezvous['shard_id'],
            engine=rendezvous['engine'],
            **kwargs
        )

        blob_name_checksum = blob_name + "_checksum"
        comparison_net.SumSqrElements(
            [blob_name], [blob_name_checksum], average=False
        )

        blob_name_gather = blob_name + "_gather"
        comparison_net.Mul(
            inputs=["compare_arr", blob_name_checksum],
            outputs=blob_name_gather,
            broadcast=1
        )

        comparison_net.Allreduce(
            inputs=[comm_world, blob_name_gather],
            outputs=[blob_name_gather],
            engine=rendezvous['engine'],
        )

        workspace.RunNetOnce(comparison_net)
        gather_arr = workspace.FetchBlob(blob_name_gather)

        baseline = gather_arr[0]
        for i in range(rendezvous['num_shards']):
            assert gather_arr[i] == baseline, \
                "allcompare failed on shard {}.".format(rendezvous['shard_id'])

        return True
