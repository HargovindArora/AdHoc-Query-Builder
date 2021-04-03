from .user_views import SignupApi, LoginApi, LogoutApi


def initialize_routes(api):
    api.add_resource(SignupApi, '/signup')
    api.add_resource(LoginApi, '/login')
    api.add_resource(LogoutApi, '/logout')
