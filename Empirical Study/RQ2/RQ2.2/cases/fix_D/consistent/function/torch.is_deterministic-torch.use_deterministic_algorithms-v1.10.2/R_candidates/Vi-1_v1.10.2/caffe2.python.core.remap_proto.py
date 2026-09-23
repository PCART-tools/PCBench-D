def remap_proto(argument, blob_remap):
    subnet = Net(argument.n)

    cloned_sub_net = subnet.Clone(
        'cloned_sub_net',
        blob_remap,
    )

    argument.n.CopyFrom(cloned_sub_net.Proto())
