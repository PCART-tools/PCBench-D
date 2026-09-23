def AddDistributedBlobSync(model, blobs):
    '''
    Sync blobs across machines (but not across devices)
    '''
    if model._rendezvous is None:
        return
    synth_name = "_".join([str(b) for b in blobs])
    comm_world = _CreateOrCloneCommonWorld(
        model.param_init_net,
        "blob_sync_cw_" + synth_name,
        rendezvous=model._rendezvous,
    )

    model.net.Allreduce(
        inputs=[comm_world] + blobs,
        outputs=blobs,
        engine=model._rendezvous['engine'],
    )
