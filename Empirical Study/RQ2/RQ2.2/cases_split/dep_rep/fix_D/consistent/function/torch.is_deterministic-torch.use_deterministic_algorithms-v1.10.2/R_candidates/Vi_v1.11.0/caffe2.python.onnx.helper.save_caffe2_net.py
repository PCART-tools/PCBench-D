def save_caffe2_net(net, file, output_txt=False):
    with open(file, "wb") as f:
        f.write(net.SerializeToString())
    if output_txt:
        with open(file + "txt", "w") as f:
            f.write(str(net))
