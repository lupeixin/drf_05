from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):
    error = "%s %s %s" % (context['view'], context['request'].method, exc)

    # 先调用drf自身的异常处理方法
    response = drf_exception_handler(exc, context)

    if response is None:
        return Response(
            {"error_message": "尊敬的上帝请稍等，后台程序猿小哥哥正在飞速处理中！"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,exception=None)

    return response
