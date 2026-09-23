def save_to_s3(tags):
    table_content = ""
    client = boto3.client("s3")
    for t in tags:
        table_content += (
            "<tr><td>{repo}</td><td>{tag}</td><td>{size}</td>"
            "<td>{last_updated_at}</td><td>{last_updated_by}</td></tr>"
        ).format(
            repo=t.repo,
            tag=t.tag,
            size=t.size,
            last_updated_at=t.last_updated_at,
            last_updated_by=t.last_updated_by,
        )
    html_body = """
    <html>
        <head>
            <link rel="stylesheet"
                href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
                integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh"
                crossorigin="anonymous">
            <link rel="stylesheet" type="text/css"
                href="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.css">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js">
            </script>
            <script type="text/javascript" charset="utf8"
                src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.js"></script>
            <title> docker image info</title>
        </head>
        <body>
            <table class="table table-striped table-hover" id="docker">
            <caption>Docker images on docker hub</caption>
            <thead class="thead-dark">
                <tr>
                <th scope="col">repo</th>
                <th scope="col">tag</th>
                <th scope="col">size</th>
                <th scope="col">last_updated_at</th>
                <th scope="col">last_updated_by</th>
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
            }} );py
        </script>
    </html>
    """.format(
        table_content=table_content
    )
    client.put_object(
        Bucket="docker.pytorch.org",
        ACL="public-read",
        Key="docker_hub.html",
        Body=html_body,
        ContentType="text/html",
    )
