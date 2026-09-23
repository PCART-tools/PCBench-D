def create_test(output_dir, width, height, default_bound, minsize, crop, means,
                stds, count, label_type, num_labels, output1=None,
                output2_size=None):
    print("Creating a temporary lmdb database of %d pictures..." % (count))

    if default_bound is None:
        default_bound = [-1] * 4

    LMDB_MAP_SIZE = 1 << 40
    env = lmdb.open(output_dir, map_size=LMDB_MAP_SIZE, subdir=True)
    index = 0
    # Create images and the expected results
    expected_results = []
    with env.begin(write=True) as txn:
        while index < count:
            img_array = np.random.random_integers(
                0, 255, [height, width, 3]).astype(np.uint8)
            img_obj = Image.fromarray(img_array)
            img_str = io.BytesIO()
            img_obj.save(img_str, 'PNG')

            # Create a random bounding box for every other image
            # ymin, xmin, bound_height, bound_width
            # TODO: To ensure that we never need to scale, we
            # ensure that the bounding-box is larger than the
            # minsize parameter
            bounding_box = list(default_bound)
            do_default_bound = True
            if index % 2 == 0:
                if height > minsize and width > minsize:
                    do_default_bound = False
                    bounding_box[0:2] = [np.random.randint(a) for a in
                                         (height - minsize, width - minsize)]
                    bounding_box[2:4] = [np.random.randint(a) + minsize for a in
                                         (height - bounding_box[0] - minsize + 1,
                                          width - bounding_box[1] - minsize + 1)]
                    # print("Bounding box is %s" % (str(bounding_box)))
            # Create expected result
            img_expected = img_array.astype(np.float32) * (1.0 / 255.0)
            # print("Orig image: %s" % (str(caffe2_img(img_expected))))
            img_expected = verify_apply_bounding_box(
                img_expected,
                bounding_box)
            # print("Bounded image: %s" % (str(caffe2_img(img_expected))))

            img_expected = verify_rescale(img_expected, minsize)

            img_expected = verify_crop(img_expected, crop)
            # print("Crop image: %s" % (str(caffe2_img(img_expected))))

            img_expected = verify_color_normalize(img_expected, means, stds)
            # print("Color image: %s" % (str(caffe2_img(img_expected))))

            tensor_protos = caffe2_pb2.TensorProtos()
            image_tensor = tensor_protos.protos.add()
            image_tensor.data_type = 4  # string data
            image_tensor.string_data.append(img_str.getvalue())
            img_str.close()

            label_tensor = tensor_protos.protos.add()
            label_tensor.data_type = 2  # int32 data
            assert (label_type >= 0 and label_type <= 3)
            if label_type == 0:
                label_tensor.int32_data.append(index)
                expected_label = index
            elif label_type == 1:
                binary_labels = np.random.randint(2, size=num_labels)
                for idx, val in enumerate(binary_labels.tolist()):
                    if val == 1:
                        label_tensor.int32_data.append(idx)
                expected_label = binary_labels
            elif label_type == 2:
                embedding_label = np.random.randint(100, size=num_labels)
                for _idx, val in enumerate(embedding_label.tolist()):
                    label_tensor.int32_data.append(val)
                expected_label = embedding_label
            elif label_type == 3:
                weight_tensor = tensor_protos.protos.add()
                weight_tensor.data_type = 1  # float weights
                binary_labels = np.random.randint(2, size=num_labels)
                expected_label = np.zeros(num_labels).astype(np.float32)
                for idx, val in enumerate(binary_labels.tolist()):
                    expected_label[idx] = val * idx
                    if val == 1:
                        label_tensor.int32_data.append(idx)
                        weight_tensor.float_data.append(idx)

            if output1:
                output1_tensor = tensor_protos.protos.add()
                output1_tensor.data_type = 1  # float data
                output1_tensor.float_data.append(output1)

            output2 = []
            if output2_size:
                output2_tensor = tensor_protos.protos.add()
                output2_tensor.data_type = 2  # int32 data
                values = np.random.randint(1024, size=output2_size)
                for val in values.tolist():
                    output2.append(val)
                    output2_tensor.int32_data.append(val)

            expected_results.append(
                [caffe2_img(img_expected), expected_label, output1, output2])

            if not do_default_bound:
                bounding_tensor = tensor_protos.protos.add()
                bounding_tensor.data_type = 2  # int32 data
                bounding_tensor.int32_data.extend(bounding_box)

            txn.put(
                '{}'.format(index).encode('ascii'),
                tensor_protos.SerializeToString()
            )
            index = index + 1
        # End while
    # End with
    return expected_results
