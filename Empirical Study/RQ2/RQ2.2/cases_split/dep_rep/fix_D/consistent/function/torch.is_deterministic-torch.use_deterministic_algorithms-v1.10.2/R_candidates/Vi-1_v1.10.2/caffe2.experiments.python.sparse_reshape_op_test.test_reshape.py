def test_reshape(old_shape, new_shape, stride_only=False):
    blob_in0 = 'col'
    blob_out0 = 'col_out'

    blob_in1 = 'row'
    blob_out1 = 'row_out'

    old_shape_for_op = (-1, old_shape[1]) if stride_only else old_shape

    op = core.CreateOperator('SparseMatrixReshape',
                             [blob_in0, blob_in1],
                             [blob_out0, blob_out1],
                             old_shape=old_shape_for_op,
                             new_shape=new_shape)

    A = np.random.random_sample(old_shape)
    A[np.random.random_sample(old_shape) > .5] = 0
    A_coo = coo_matrix(A)
    old_row, old_col = A_coo.row, A_coo.col

    workspace.FeedBlob(blob_in0, old_col.astype(np.int64))
    workspace.FeedBlob(blob_in1, old_row.astype(np.int32))

    workspace.RunOperatorOnce(op)

    A_new_coo = coo_matrix(A.reshape(new_shape))
    new_row, new_col = A_new_coo.row, A_new_coo.col

    col_out = workspace.FetchBlob(blob_out0)
    row_out = workspace.FetchBlob(blob_out1)

    np.testing.assert_array_equal(col_out, new_col)
    np.testing.assert_array_equal(row_out, new_row)
