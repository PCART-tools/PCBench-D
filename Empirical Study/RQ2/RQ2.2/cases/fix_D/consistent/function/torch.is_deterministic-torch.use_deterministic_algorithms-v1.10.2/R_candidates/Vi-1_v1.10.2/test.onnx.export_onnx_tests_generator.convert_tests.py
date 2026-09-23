def convert_tests(testcases, sets=1):
    print("Collect {} test cases from PyTorch.".format(len(testcases)))
    failed = 0
    FunctionalModule_nums = 0
    nn_module = {}
    for t in testcases:
        test_name = get_test_name(t)
        module = gen_module(t)
        module_name = str(module).split("(")[0]
        if (module_name == "FunctionalModule"):
            FunctionalModule_nums += 1
        else:
            if (module_name not in nn_module):
                nn_module[module_name] = 0
        try:
            input = gen_input(t)
            f = io.BytesIO()
            torch.onnx._export(module, input, f,
                               operator_export_type=torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK)
            onnx_model = onnx.load_from_string(f.getvalue())
            onnx.checker.check_model(onnx_model)
            onnx.helper.strip_doc_string(onnx_model)
            output_dir = os.path.join(test_onnx_common.pytorch_converted_dir, test_name)

            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
            os.makedirs(output_dir)
            with open(os.path.join(output_dir, "model.onnx"), "wb") as file:
                file.write(onnx_model.SerializeToString())

            for i in range(sets):
                output = module(input)
                data_dir = os.path.join(output_dir, "test_data_set_{}".format(i))
                os.makedirs(data_dir)

                for index, var in enumerate([input]):
                    tensor = numpy_helper.from_array(var.data.numpy())
                    with open(os.path.join(data_dir, "input_{}.pb".format(index)), "wb") as file:
                        file.write(tensor.SerializeToString())
                for index, var in enumerate([output]):
                    tensor = numpy_helper.from_array(var.data.numpy())
                    with open(os.path.join(data_dir, "output_{}.pb".format(index)), "wb") as file:
                        file.write(tensor.SerializeToString())
                input = gen_input(t)
                if (module_name != "FunctionalModule"):
                    nn_module[module_name] |= 1
        except:  # noqa: E722,B001
            traceback.print_exc()
            if (module_name != "FunctionalModule"):
                nn_module[module_name] |= 2
            failed += 1

    print("Collect {} test cases from PyTorch repo, failed to export {} cases.".format(
        len(testcases), failed))
    print("PyTorch converted cases are stored in {}.".format(test_onnx_common.pytorch_converted_dir))
    print_stats(FunctionalModule_nums, nn_module)
