@cli.command("tensorboard-graphs")
@click.option("--c2-netdef", type=click.Path(exists=True, dir_okay=False),
              multiple=True)
@click.option("--tf-dir", type=click.Path(exists=True))
def tensorboard_graphs(c2_netdef, tf_dir):
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)

    def parse_net_def(path):
        import google.protobuf.text_format  # type: ignore[import]
        net_def = caffe2_pb2.NetDef()
        with open(path) as f:
            google.protobuf.text_format.Merge(f.read(), net_def)
        return core.Net(net_def)

    graph_defs = [tb_exporter.nets_to_graph_def([parse_net_def(path)])
                  for path in c2_netdef]
    events = [graph_def_to_event(i, graph_def)
              for (i, graph_def) in enumerate(graph_defs, start=1)]
    write_events(tf_dir, events)
    log.info("Wrote %s graphs to logdir %s", len(events), tf_dir)
