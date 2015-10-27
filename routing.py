from view import user, project, host, auth, example

def generate_routes(app, settings):
    app.add_route("/v1/auth", auth.Authentication(settings))

    app.add_route("/v1/user", user.Collection(settings))
    app.add_route("/v1/user/{user}", user.Item(settings))

    app.add_route("/v1/host", host.Collection(settings))

    app.add_route("/v1/project/", project.Collection(settings))
    app.add_route("/v1/project/{project_name}/", project.Item(settings))

    app.add_route("/v1/project/{project_name}/example/", example.Collection(settings))


