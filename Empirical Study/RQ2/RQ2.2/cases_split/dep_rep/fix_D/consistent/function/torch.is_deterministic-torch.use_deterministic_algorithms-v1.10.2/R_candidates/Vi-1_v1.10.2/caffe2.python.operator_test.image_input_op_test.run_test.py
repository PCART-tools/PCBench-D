def run_test(
        size_tuple, means, stds, label_type, num_labels, is_test, scale_jitter_type,
        color_jitter, color_lighting, dc, validator, output1=None, output2_size=None):
    # TODO: Does not test on GPU and does not test use_gpu_transform
    # WARNING: Using ModelHelper automatically does NHWC to NCHW
    # transformation if needed.
    width, height, minsize, crop = size_tuple
    means = [float(m) for m in means]
    stds = [float(s) for s in stds]
    out_dir = tempfile.mkdtemp()
    count_images = 2  # One with bounding box and one without
    expected_images = create_test(
        out_dir,
        width=width,
        height=height,
        default_bound=(3, 5, height - 3, width - 5),
        minsize=minsize,
        crop=crop,
        means=means,
        stds=stds,
        count=count_images,
        label_type=label_type,
        num_labels=num_labels,
        output1=output1,
        output2_size=output2_size
    )
    for device_option in dc:
        with hu.temp_workspace():
            reader_net = core.Net('reader')
            reader_net.CreateDB(
                [],
                'DB',
                db=out_dir,
                db_type="lmdb"
            )
            workspace.RunNetOnce(reader_net)
            outputs = ['data', 'label']
            output_sizes = []
            if output1:
                outputs.append('output1')
                output_sizes.append(1)
            if output2_size:
                outputs.append('output2')
                output_sizes.append(output2_size)
            imageop = core.CreateOperator(
                'ImageInput',
                ['DB'],
                outputs,
                batch_size=count_images,
                color=3,
                minsize=minsize,
                crop=crop,
                is_test=is_test,
                bounding_ymin=3,
                bounding_xmin=5,
                bounding_height=height - 3,
                bounding_width=width - 5,
                mean_per_channel=means,
                std_per_channel=stds,
                use_gpu_transform=(device_option.device_type == 1),
                label_type=label_type,
                num_labels=num_labels,
                output_sizes=output_sizes,
                scale_jitter_type=scale_jitter_type,
                color_jitter=color_jitter,
                color_lighting=color_lighting
            )

            imageop.device_option.CopyFrom(device_option)
            main_net = core.Net('main')
            main_net.Proto().op.extend([imageop])
            workspace.RunNetOnce(main_net)
            validator(expected_images, device_option, count_images)
            # End for
        # End with
    # End for
    shutil.rmtree(out_dir)
