def run_in_hip(gc, dc):
    return (gc.device_type == caffe2_pb2.HIP) or (
        caffe2_pb2.HIP in {d.device_type for d in dc})
