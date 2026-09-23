def quant_type_to_str(quant_type):
    m = {
        QuantType.STATIC: "static",
        QuantType.DYNAMIC: "dynamic",
        QuantType.QAT: "qat",
        QuantType.WEIGHT_ONLY: "weight_only",
    }
    return m[quant_type]
