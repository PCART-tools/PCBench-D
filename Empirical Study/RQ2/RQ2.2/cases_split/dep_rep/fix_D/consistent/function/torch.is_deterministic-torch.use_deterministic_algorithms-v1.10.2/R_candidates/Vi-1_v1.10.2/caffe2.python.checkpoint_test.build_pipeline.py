def build_pipeline(node_id):
    with Node('trainer_%d' % node_id):
        with Job.current().init_group, Task():
            data_arr = Struct(('val', np.array(list(range(10)))))
            data = ConstRecord(ops, data_arr)
            ds = Dataset(data, name='dataset:%d' % node_id)
            full_reader = ds.reader(ops)
            total = ops.Const([100])

        def inc_total(rec):
            ops.Add([total, rec.val()], [total])

        epoch_reader = ReaderWithLimit(full_reader, num_iter=3)
        pipe(epoch_reader, processor=inc_total)
        Job.current().add_stop_condition(epoch_reader.data_finished())
    return [total]
