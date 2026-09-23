def save_to_s3(project, data):
    table_content = ""
    client = boto3.client("s3")
    for repo, tag, window, age, pushed in data:
        table_content += "<tr><td>{repo}</td><td>{tag}</td><td>{window}</td><td>{age}</td><td>{pushed}</td></tr>".format(
            repo=repo, tag=tag, window=window, age=age, pushed=pushed
        )
    html_body = """
    <html>
        <head>
            <link rel="stylesheet"
                href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
                integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh"
                crossorigin="anonymous">
            <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.css">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
            <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.js"></script>
            <title>{project} nightly and permanent docker image info</title>
        </head>
        <body>
            <table class="table table-striped table-hover" id="docker">
            <thead class="thead-dark">
                <tr>
                <th scope="col">repo</th>
                <th scope="col">tag</th>
                <th scope="col">keep window</th>
                <th scope="col">age</th>
                <th scope="col">pushed at</th>
                </tr>
            </thead>
            <tbody>
                {table_content}
            </tbody>
            </table>
        </body>
        <script>
            $(document).ready( function () {{
                $('#docker').DataTable({{paging: false}});
            }} );
        </script>
    </html>
    """.format(
        project=project, table_content=table_content
    )

    # for pytorch, file can be found at
    # http://ossci-docker.s3-website.us-east-1.amazonaws.com/pytorch.html
    # and later one we can config docker.pytorch.org to point to the location

    client.put_object(
        Bucket="docker.pytorch.org",
        ACL="public-read",
        Key="{project}.html".format(project=project),
        Body=html_body,
        ContentType="text/html",
    )
