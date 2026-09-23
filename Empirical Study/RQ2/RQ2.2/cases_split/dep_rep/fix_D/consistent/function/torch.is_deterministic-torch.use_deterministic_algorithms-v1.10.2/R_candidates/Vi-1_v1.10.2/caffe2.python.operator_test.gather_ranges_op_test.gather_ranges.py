def gather_ranges(data, ranges):
    lengths = []
    output = []
    for example_ranges in ranges:
        length = 0
        for range in example_ranges:
            assert len(range) == 2
            output.extend(data[range[0] : range[0] + range[1]])
            length += range[1]
        lengths.append(length)
    return output, lengths
