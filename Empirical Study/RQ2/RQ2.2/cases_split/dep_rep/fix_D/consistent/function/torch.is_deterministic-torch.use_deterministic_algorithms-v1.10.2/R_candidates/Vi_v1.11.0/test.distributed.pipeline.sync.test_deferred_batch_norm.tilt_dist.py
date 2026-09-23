def tilt_dist(input):
    # Tilt variance by channel.
    rgb = input.transpose(0, 1)
    rgb[0] *= 1
    rgb[1] *= 10
    rgb[2] *= 100

    # Tilt mean by single batch.
    for i, single in enumerate(input):
        single += 2 ** i

    return input
