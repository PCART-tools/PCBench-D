def build_access_token(username, passwordtr):
    r = requests.post(
        "https://hub.docker.com/v2/users/login/",
        data={"username": username, "password": password},
    )
    r.raise_for_status()
    token = r.json().get("token")
    return {"Authorization": "JWT " + token}
