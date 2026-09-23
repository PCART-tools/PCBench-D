def jsonify_nvd3(chart):
    chart.buildcontent()
    # Note(Yangqing): python-nvd3 does not seem to separate the built HTML part
    # and the script part. Luckily, it seems to be the case that the HTML part is
    # only a <div>, which can be accessed by chart.container; the script part,
    # while the script part occupies the rest of the html content, which we can
    # then find by chart.htmlcontent.find['<script>'].
    script_start = chart.htmlcontent.find('<script>') + 8
    script_end = chart.htmlcontent.find('</script>')
    return flask.jsonify(
        result=chart.container,
        script=chart.htmlcontent[script_start:script_end].strip()
    )
