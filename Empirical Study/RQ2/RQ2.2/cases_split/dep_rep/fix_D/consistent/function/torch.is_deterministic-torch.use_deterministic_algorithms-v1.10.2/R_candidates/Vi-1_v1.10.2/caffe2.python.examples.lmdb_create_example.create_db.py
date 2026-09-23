def create_db(output_file):
    print(">>> Write database...")
    LMDB_MAP_SIZE = 1 << 40   # MODIFY
    env = lmdb.open(output_file, map_size=LMDB_MAP_SIZE)

    checksum = 0
    with env.begin(write=True) as txn:
        for j in range(0, 128):
            # MODIFY: add your own data reader / creator
            label = j % 10
            width = 64
            height = 32

            img_data = np.random.rand(3, width, height)
            # ...

            # Create TensorProtos
            tensor_protos = caffe2_pb2.TensorProtos()
            img_tensor = tensor_protos.protos.add()
            img_tensor.dims.extend(img_data.shape)
            img_tensor.data_type = 1

            flatten_img = img_data.reshape(np.prod(img_data.shape))
            img_tensor.float_data.extend(flatten_img)

            label_tensor = tensor_protos.protos.add()
            label_tensor.data_type = 2
            label_tensor.int32_data.append(label)
            txn.put(
                '{}'.format(j).encode('ascii'),
                tensor_protos.SerializeToString()
            )

            checksum += np.sum(img_data) * label
            if (j % 16 == 0):
                print("Inserted {} rows".format(j))

    print("Checksum/write: {}".format(int(checksum)))
    return checksum
