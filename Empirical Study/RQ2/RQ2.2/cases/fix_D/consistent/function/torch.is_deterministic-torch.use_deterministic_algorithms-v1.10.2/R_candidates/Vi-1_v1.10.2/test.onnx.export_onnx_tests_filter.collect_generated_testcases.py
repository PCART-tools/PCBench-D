def collect_generated_testcases(root_dir=test_onnx_common.pytorch_converted_dir,
                                verbose=False, fail_dir=None, expect=True):
    total_pass = 0
    total_fail = 0
    for d in os.listdir(root_dir):
        dir_name = os.path.join(root_dir, d)
        if os.path.isdir(dir_name):
            failed = False
            try:
                model_file = os.path.join(dir_name, "model.onnx")
                data_dir_pattern = os.path.join(dir_name, "test_data_set_*")
                for data_dir in glob.glob(data_dir_pattern):
                    for device in torch.testing.get_all_device_types():
                        run_generated_test(model_file, data_dir, device)
                if expect:
                    expect_file = os.path.join(_expect_dir,
                                               "PyTorch-generated-{}.expect".format(d))
                    with open(expect_file, "w") as text_file:
                        model = onnx.load(model_file)
                        onnx.checker.check_model(model)
                        onnx.helper.strip_doc_string(model)
                        text_file.write(google.protobuf.text_format.MessageToString(model))
                total_pass += 1
            except Exception as e:
                if verbose:
                    print("The test case in {} failed!".format(dir_name))
                    traceback.print_exc()
                if fail_dir is None:
                    shutil.rmtree(dir_name)
                else:
                    target_dir = os.path.join(fail_dir, d)
                    if os.path.exists(target_dir):
                        shutil.rmtree(target_dir)
                    shutil.move(dir_name, target_dir)
                total_fail += 1
    print("Successfully generated/updated {} test cases from PyTorch.".format(total_pass))
    if expect:
        print("Expected pbtxt files are generated in {}.".format(_expect_dir))
    print("Failed {} testcases are moved to {}.".format(total_fail, _fail_test_dir))
