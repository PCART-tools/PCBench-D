def _AllReduceBlobs(blob_names, devices, model, net, rendezvous, use_nccl,
                    max_concurrent_distributed_ops):
    if rendezvous is None or rendezvous['num_shards'] <= 1:
        _AllReduceBlobsSingleHost(
            blob_names,
            devices,
            model,
            net,
            use_nccl
        )
    else:
        _AllReduceBlobsDistributed(
            blob_names,
            devices,
            model,
            net,
            rendezvous,
            max_concurrent_distributed_ops,
        )
