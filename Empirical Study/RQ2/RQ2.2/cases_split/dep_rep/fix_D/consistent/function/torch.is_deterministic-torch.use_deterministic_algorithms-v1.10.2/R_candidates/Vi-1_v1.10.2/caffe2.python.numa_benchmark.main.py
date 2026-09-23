def main():
    assert workspace.IsNUMAEnabled() and workspace.GetNumNUMANodes() >= 2

    single_init, single_net = build_net("single_net", False)
    cross_init, cross_net = build_net("cross_net", True)

    workspace.CreateNet(single_init)
    workspace.RunNet(single_init.Name())
    workspace.CreateNet(cross_init)
    workspace.RunNet(cross_init.Name())

    workspace.CreateNet(single_net)
    workspace.CreateNet(cross_net)

    for _ in range(4):
        t = time.time()
        workspace.RunNet(single_net.Name(), NUM_ITER)
        dt = time.time() - t
        print("Single socket time:", dt)
        single_bw = 4 * SHAPE_LEN * SHAPE_LEN * NUM_REPLICAS * NUM_ITER / dt / GB
        print("Single socket BW: {} GB/s".format(single_bw))

        t = time.time()
        workspace.RunNet(cross_net.Name(), NUM_ITER)
        dt = time.time() - t
        print("Cross socket time:", dt)
        cross_bw = 4 * SHAPE_LEN * SHAPE_LEN * NUM_REPLICAS * NUM_ITER / dt / GB
        print("Cross socket BW: {} GB/s".format(cross_bw))
        print("Single BW / Cross BW: {}".format(single_bw / cross_bw))
