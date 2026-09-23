def padding2d_circular(input, pad):
    r"""input:
             [[[[0., 1., 2],
                [3., 4., 5.]]]]
            pad: (1, 2, 2, 1)
    output:
        [[[[2., 0., 1., 2., 0., 1.],
           [5., 3., 4., 5., 3., 4.],
           [2., 0., 1., 2., 0., 1.],
           [5., 3., 4., 5., 3., 4.],
           [2., 0., 1., 2., 0., 1.]]]]
    """
    input = torch.cat([input[:, :, -pad[2]:], input, input[:, :, 0:pad[3]]], dim=2)
    return torch.cat([input[:, :, :, -pad[0]:], input, input[:, :, :, 0:pad[1]]], dim=3)
