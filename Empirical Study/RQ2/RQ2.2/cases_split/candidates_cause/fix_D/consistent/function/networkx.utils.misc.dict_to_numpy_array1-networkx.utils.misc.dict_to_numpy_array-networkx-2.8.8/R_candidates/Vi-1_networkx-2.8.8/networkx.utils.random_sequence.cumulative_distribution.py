def cumulative_distribution(distribution):
    """Returns normalized cumulative distribution from discrete distribution."""

    cdf = [0.0]
    psum = sum(distribution)
    for i in range(0, len(distribution)):
        cdf.append(cdf[i] + distribution[i] / psum)
    return cdf
