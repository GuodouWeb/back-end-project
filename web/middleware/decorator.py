import json

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from web.uilts.Jwt import UserToken

FORBIDDEN = "对不起, 你没有足够的权限"

TOKEN_WHITELIST = [
    '/api/user/register',
    '/api/get_userinfo',
    '/api/ref_token',
]
SESSION_WHITELIST = [
    '/api/login',
]


class Permission(MiddlewareMixin):

    def process_request(self, request):
        try:
            if request.path_info not in TOKEN_WHITELIST:
                return
            headers = request.headers
            token = headers.get('token')
            if token is None:
                return HttpResponse(json.dumps({'code': 404, 'msg': "用户信息认证失败"}),
                                    content_type="application/json;charset=UTF-8")
            # get userInfo
            user_info = UserToken.parse_token(token)
            data = request.POST.copy()
            data["user_info"] = user_info
            request.POST = data
        except:
            return HttpResponse(json.dumps({'code': 404, 'msg': "用户信息认证失败"}),
                                content_type="application/json;charset=UTF-8")
