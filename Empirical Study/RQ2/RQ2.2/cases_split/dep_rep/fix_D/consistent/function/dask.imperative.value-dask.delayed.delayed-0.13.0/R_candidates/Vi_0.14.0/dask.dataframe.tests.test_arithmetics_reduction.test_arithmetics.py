@pytest.mark.slow
def test_arithmetics():
    dsk = {('x', 0): pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]},
                                  index=[0, 1, 3]),
           ('x', 1): pd.DataFrame({'a': [4, 5, 6], 'b': [3, 2, 1]},
                                  index=[5, 6, 8]),
           ('x', 2): pd.DataFrame({'a': [7, 8, 9], 'b': [0, 0, 0]},
                                  index=[9, 9, 9])}
    meta = make_meta({'a': 'i8', 'b': 'i8'}, index=pd.Index([], 'i8'))
    ddf1 = dd.DataFrame(dsk, 'x', meta, [0, 4, 9, 9])
    pdf1 = ddf1.compute()

    pdf2 = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6, 7, 8],
                         'b': [5, 6, 7, 8, 1, 2, 3, 4]})
    pdf3 = pd.DataFrame({'a': [5, 6, 7, 8, 4, 3, 2, 1],
                         'b': [2, 4, 5, 3, 4, 2, 1, 0]})
    ddf2 = dd.from_pandas(pdf2, 3)
    ddf3 = dd.from_pandas(pdf3, 2)

    dsk4 = {('y', 0): pd.DataFrame({'a': [3, 2, 1], 'b': [7, 8, 9]},
                                   index=[0, 1, 3]),
            ('y', 1): pd.DataFrame({'a': [5, 2, 8], 'b': [4, 2, 3]},
                                   index=[5, 6, 8]),
            ('y', 2): pd.DataFrame({'a': [1, 4, 10], 'b': [1, 0, 5]},
                                   index=[9, 9, 9])}
    ddf4 = dd.DataFrame(dsk4, 'y', meta, [0, 4, 9, 9])
    pdf4 = ddf4.compute()

    # Arithmetics
    cases = [(ddf1, ddf1, pdf1, pdf1),
             (ddf1, ddf1.repartition([0, 1, 3, 6, 9]), pdf1, pdf1),
             (ddf2, ddf3, pdf2, pdf3),
             (ddf2.repartition([0, 3, 6, 7]), ddf3.repartition([0, 7]),
              pdf2, pdf3),
             (ddf2.repartition([0, 7]), ddf3.repartition([0, 2, 4, 5, 7]),
              pdf2, pdf3),
             (ddf1, ddf4, pdf1, pdf4),
             (ddf1, ddf4.repartition([0, 9]), pdf1, pdf4),
             (ddf1.repartition([0, 3, 9]), ddf4.repartition([0, 5, 9]),
              pdf1, pdf4),
             # dask + pandas
             (ddf1, pdf4, pdf1, pdf4), (ddf2, pdf3, pdf2, pdf3)]

    for (l, r, el, er) in cases:
        check_series_arithmetics(l.a, r.b, el.a, er.b)
        check_frame_arithmetics(l, r, el, er)

    # different index, pandas raises ValueError in comparison ops

    pdf5 = pd.DataFrame({'a': [3, 2, 1, 5, 2, 8, 1, 4, 10],
                         'b': [7, 8, 9, 4, 2, 3, 1, 0, 5]},
                        index=[0, 1, 3, 5, 6, 8, 9, 9, 9])
    ddf5 = dd.from_pandas(pdf5, 2)

    pdf6 = pd.DataFrame({'a': [3, 2, 1, 5, 2, 8, 1, 4, 10],
                         'b': [7, 8, 9, 5, 7, 8, 4, 2, 5]},
                        index=[0, 1, 2, 3, 4, 5, 6, 7, 9])
    ddf6 = dd.from_pandas(pdf6, 4)

    pdf7 = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6, 7, 8],
                         'b': [5, 6, 7, 8, 1, 2, 3, 4]},
                        index=list('aaabcdeh'))
    pdf8 = pd.DataFrame({'a': [5, 6, 7, 8, 4, 3, 2, 1],
                         'b': [2, 4, 5, 3, 4, 2, 1, 0]},
                        index=list('abcdefgh'))
    ddf7 = dd.from_pandas(pdf7, 3)
    ddf8 = dd.from_pandas(pdf8, 4)

    pdf9 = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6, 7, 8],
                         'b': [5, 6, 7, 8, 1, 2, 3, 4],
                         'c': [5, 6, 7, 8, 1, 2, 3, 4]},
                        index=list('aaabcdeh'))
    pdf10 = pd.DataFrame({'b': [5, 6, 7, 8, 4, 3, 2, 1],
                          'c': [2, 4, 5, 3, 4, 2, 1, 0],
                          'd': [2, 4, 5, 3, 4, 2, 1, 0]},
                         index=list('abcdefgh'))
    ddf9 = dd.from_pandas(pdf9, 3)
    ddf10 = dd.from_pandas(pdf10, 4)

    # Arithmetics with different index
    cases = [(ddf5, ddf6, pdf5, pdf6),
             (ddf5.repartition([0, 9]), ddf6, pdf5, pdf6),
             (ddf5.repartition([0, 5, 9]), ddf6.repartition([0, 7, 9]),
              pdf5, pdf6),
             (ddf7, ddf8, pdf7, pdf8),
             (ddf7.repartition(['a', 'c', 'h']), ddf8.repartition(['a', 'h']),
              pdf7, pdf8),
             (ddf7.repartition(['a', 'b', 'e', 'h']),
              ddf8.repartition(['a', 'e', 'h']), pdf7, pdf8),
             (ddf9, ddf10, pdf9, pdf10),
             (ddf9.repartition(['a', 'c', 'h']), ddf10.repartition(['a', 'h']),
              pdf9, pdf10),
             # dask + pandas
             (ddf5, pdf6, pdf5, pdf6), (ddf7, pdf8, pdf7, pdf8),
             (ddf9, pdf10, pdf9, pdf10)]

    for (l, r, el, er) in cases:
        check_series_arithmetics(l.a, r.b, el.a, er.b,
                                 allow_comparison_ops=False)
        check_frame_arithmetics(l, r, el, er,
                                allow_comparison_ops=False)
