def padding1d_circular(input, pad):
    r""" input:
            [[[0., 1., 2.],
              [3., 4., 5.]]]
          pad: (1, 2)
          output:
            [[[2., 0., 1., 2., 0., 1.],
              [5., 3., 4., 5., 3., 4.]]]
    """
    return torch.cat([input[:, :, -pad[0]:], input,
                      input[:, :, 0:pad[1]]], dim=2)
