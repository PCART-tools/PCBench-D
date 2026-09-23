@Analyzer.register(OperatorDef)
def analyze_op(analyzer, op):
    for x in op.input:
        analyzer.need_blob(x)
    for x in op.output:
        analyzer.define_blob(x)
