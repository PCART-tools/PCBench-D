@cli.command("tensorboard-events")
@click.option("--c2-dir", type=click.Path(exists=True, file_okay=False),
              help="Root directory of the Caffe2 run")
@click.option("--tf-dir", type=click.Path(writable=True),
              help="Output path to the logdir used by TensorBoard")
def tensorboard_events(c2_dir, tf_dir):
    np.random.seed(1701)
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    S = collections.namedtuple('S', ['min', 'max', 'mean', 'std'])

    def parse_summary(filename):
        try:
            with open(filename) as f:
                rows = [(float(el) for el in line.split()) for line in f]
                return [S(*r) for r in rows]
        except Exception as e:
            log.exception(e)
            return None

    def get_named_summaries(root):
        summaries = [
            (fname, parse_summary(os.path.join(dirname, fname)))
            for dirname, _, fnames in os.walk(root)
            for fname in fnames
        ]
        return [(n, s) for (n, s) in summaries if s]

    def inferred_histo(summary, samples=1000):
        np.random.seed(
            hash(
                summary.std + summary.mean + summary.min + summary.max
            ) % np.iinfo(np.int32).max
        )
        samples = np.random.randn(samples) * summary.std + summary.mean
        samples = np.clip(samples, a_min=summary.min, a_max=summary.max)
        (hist, edges) = np.histogram(samples)
        upper_edges = edges[1:]
        r = HistogramProto(
            min=summary.min,
            max=summary.max,
            num=len(samples),
            sum=samples.sum(),
            sum_squares=(samples * samples).sum())
        r.bucket_limit.extend(upper_edges)
        r.bucket.extend(hist)
        return r

    def named_summaries_to_events(named_summaries):
        names = [n for (n, _) in named_summaries]
        summaries = [s for (_, s) in named_summaries]
        summaries = list(zip(*summaries))

        def event(step, values):
            s = Summary()
            scalar = [
                Summary.Value(
                    tag="{}/{}".format(name, field),
                    simple_value=v)
                for name, value in zip(names, values)
                for field, v in value._asdict().items()]
            hist = [
                Summary.Value(
                    tag="{}/inferred_normal_hist".format(name),
                    histo=inferred_histo(value))
                for name, value in zip(names, values)
            ]
            s.value.extend(scalar + hist)
            return Event(wall_time=int(step), step=step, summary=s)

        return [event(step, values)
                for step, values in enumerate(summaries, start=1)]

    named_summaries = get_named_summaries(c2_dir)
    events = named_summaries_to_events(named_summaries)
    write_events(tf_dir, events)
    log.info("Wrote %s events to logdir %s", len(events), tf_dir)
