def test_dataframe_format_unknown_divisions():
    df = pd.DataFrame({'A': [1, 2, 3, 4, 5, 6, 7, 8],
                       'B': list('ABCDEFGH'),
                       'C': pd.Categorical(list('AAABBBCC'))})
    ddf = dd.from_pandas(df, 3)
    ddf = ddf.clear_divisions()
    assert not ddf.known_divisions

    exp = ("Dask DataFrame Structure:\n"
           "                   A       B                C\n"
           "npartitions=3                                \n"
           "None           int64  object  category[known]\n"
           "None             ...     ...              ...\n"
           "None             ...     ...              ...\n"
           "None             ...     ...              ...\n"
           "Dask Name: from_pandas, 3 tasks")
    assert repr(ddf) == exp
    assert str(ddf) == exp

    exp = ("                   A       B                C\n"
           "npartitions=3                                \n"
           "None           int64  object  category[known]\n"
           "None             ...     ...              ...\n"
           "None             ...     ...              ...\n"
           "None             ...     ...              ...")
    assert ddf.to_string() == exp

    exp_table = """<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
    </tr>
    <tr>
      <th>npartitions=3</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>None</th>
      <td>int64</td>
      <td>object</td>
      <td>category[known]</td>
    </tr>
    <tr>
      <th>None</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>None</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>None</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>"""

    exp = """<div><strong>Dask DataFrame Structure:</strong></div>
{exp_table}
<div>Dask Name: from_pandas, 3 tasks</div>""".format(exp_table=exp_table)
    assert ddf.to_html() == exp

    # table is boxed with div
    exp = """<div><strong>Dask DataFrame Structure:</strong></div>
<div>
{exp_table}
</div>
<div>Dask Name: from_pandas, 3 tasks</div>""".format(exp_table=exp_table)
    assert ddf._repr_html_() == exp
