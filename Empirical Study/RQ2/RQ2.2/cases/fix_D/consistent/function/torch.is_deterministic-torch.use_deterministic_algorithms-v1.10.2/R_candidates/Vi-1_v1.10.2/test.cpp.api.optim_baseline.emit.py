def emit(optimizer_parameter_map):
    # Don't write generated with an @ in front, else this file is recognized as generated.
    print("// @{} from {}".format('generated', __file__))
    print(HEADER)
    for optimizer_name, parameters in optimizer_parameter_map.items():
        print(PARAMETERS.format(optimizer_name))
        print("  return {")
        for sample in parameters:
            print("    {")
            for parameter in sample:
                parameter_values = "{{{}}}".format(", ".join(map(str, parameter)))
                print("      torch::tensor({}),".format(parameter_values))
            print("    },")
        print("  };")
        print("}\n")
    print(FOOTER)
