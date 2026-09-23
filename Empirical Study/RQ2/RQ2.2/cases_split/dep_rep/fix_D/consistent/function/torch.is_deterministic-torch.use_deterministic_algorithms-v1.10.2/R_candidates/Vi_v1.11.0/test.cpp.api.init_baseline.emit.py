def emit(initializer_parameter_map):
    # Don't write generated with an @ in front, else this file is recognized as generated.
    print("// @{} from {}".format('generated', __file__))
    print(HEADER)
    for initializer_name, weights in initializer_parameter_map.items():
        print(PARAMETERS.format(initializer_name))
        print("  return {")
        for sample in weights:
            print("    {")
            for parameter in sample:
                parameter_values = "{{{}}}".format(", ".join(map(str, parameter)))
                print("      torch::tensor({}),".format(parameter_values))
            print("    },")
        print("  };")
        print("}\n")
    print(FOOTER)
