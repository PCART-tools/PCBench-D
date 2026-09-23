def main():
    parser = argparse.ArgumentParser(description="Caffe2 net drawer.")
    parser.add_argument(
        "--input",
        type=str, required=True,
        help="The input protobuf file."
    )
    parser.add_argument(
        "--output_prefix",
        type=str, default="",
        help="The prefix to be added to the output filename."
    )
    parser.add_argument(
        "--minimal", action="store_true",
        help="If set, produce a minimal visualization."
    )
    parser.add_argument(
        "--minimal_dependency", action="store_true",
        help="If set, only draw minimal dependency."
    )
    parser.add_argument(
        "--append_output", action="store_true",
        help="If set, append the output blobs to the operator names.")
    parser.add_argument(
        "--rankdir", type=str, default="LR",
        help="The rank direction of the pydot graph."
    )
    args = parser.parse_args()
    with open(args.input, 'r') as fid:
        content = fid.read()
        graphs = utils.GetContentFromProtoString(
            content, {
                caffe2_pb2.PlanDef: lambda x: GetOperatorMapForPlan(x),
                caffe2_pb2.NetDef: lambda x: {x.name: x.op},
            }
        )
    for key, operators in viewitems(graphs):
        if args.minimal:
            graph = GetPydotGraphMinimal(
                operators,
                name=key,
                rankdir=args.rankdir,
                node_producer=GetOpNodeProducer(args.append_output, **OP_STYLE),
                minimal_dependency=args.minimal_dependency)
        else:
            graph = GetPydotGraph(
                operators,
                name=key,
                rankdir=args.rankdir,
                node_producer=GetOpNodeProducer(args.append_output, **OP_STYLE))
        filename = args.output_prefix + graph.get_name() + '.dot'
        graph.write(filename, format='raw')
        pdf_filename = filename[:-3] + 'pdf'
        try:
            graph.write_pdf(pdf_filename)
        except Exception:
            print(
                'Error when writing out the pdf file. Pydot requires graphviz '
                'to convert dot files to pdf, and you may not have installed '
                'graphviz. On ubuntu this can usually be installed with "sudo '
                'apt-get install graphviz". We have generated the .dot file '
                'but will not be able to generate pdf file for now.'
            )
