def ConvertProtoToBinary(proto_class, filename, out_filename):
    """Convert a text file of the given protobuf class to binary."""
    with open(filename) as f:
        proto = TryReadProtoWithClass(proto_class, f.read())
    with open(out_filename, 'w') as fid:
        fid.write(proto.SerializeToString())
