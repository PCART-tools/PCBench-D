def gh_labels(pr_number):
    query = f"""
    {{
      repository(owner: "pytorch", name: "pytorch") {{
        pullRequest(number: {pr_number}) {{
          labels(first: 10) {{
            edges {{
              node {{
                name
              }}
            }}
          }}
        }}
      }}
    }}
    """
    query = run_query(query)
    edges = query['data']['repository']['pullRequest']['labels']['edges']
    return [edge['node']['name'] for edge in edges]
