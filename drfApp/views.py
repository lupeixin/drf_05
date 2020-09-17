from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from drfApp.models import Student
from drfApp.serializers import StudentModelSerializer
from utils.response import APIResponse


class StudentAPIView(APIView):

    def patch(self, request, *args, **kwargs):
        """
        群改接口
        :param request:
        :return:
        """
        request_data = request.data
        student_id = kwargs.get("id")
        if student_id and isinstance(request_data, dict):
            student_ids = [student_id, ]
            request_data = [request_data]
        elif not student_id and isinstance(request_data, list):
            student_ids = []
            for dic in request_data:
                id = dic.pop("id", None)
                if id:
                    student_ids.append(id)
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": 'id不存在',
                    })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": '参数有误',
            })

        student_list = []
        for pk in student_ids:
            try:
                student_obj = Student.objects.get(pk=pk)
                student_list.append(student_obj)
            except:
                index = student_ids.index(pk)
                request_data.pop(index)
        student_ser = StudentModelSerializer(data=request_data,
                                             instance=student_list,
                                             partial=True,
                                             context={"request": request},
                                             many=True)
        student_ser.is_valid(raise_exception=True)
        student_ser.save()
        return Response({
            "status": status.HTTP_200_OK,
            "message": "批量更新成功",
        })


class StudentGenericAPIView(ListModelMixin,
                            RetrieveModelMixin,
                            CreateModelMixin,
                            UpdateModelMixin,
                            DestroyModelMixin,
                            GenericAPIView):
    # 获取当前视图操作的模型的数据  以及序列化器类
    queryset = Student.objects.filter(is_delete=False)
    serializer_class = StudentModelSerializer

    # 指定查询单个对象的参数
    lookup_field = "id"

    # 查询接口
    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    # 新增图书
    def post(self, request, *args, **kwargs):
        create = self.create(request, *args, **kwargs)
        return APIResponse(results=create.data, data_message="新增方便")

    # 单整体改
    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return APIResponse(results=response.data)

    # 更新单个
    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return APIResponse(results=response.data)

    # 删除单个
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class StudentGenericMixinView(ListAPIView, RetrieveAPIView, CreateAPIView):
    queryset = Student.objects.filter(is_delete=False)
    serializer_class = StudentModelSerializer
    lookup_field = "id"


class StudentModelViewSet(ModelViewSet, StudentAPIView):
    queryset = Student.objects.filter(is_delete=False)
    serializer_class = StudentModelSerializer
    lookup_field = "id"

    """定义登录操作"""

    def student_login(self, request, *args, **kwargs):
        # 可以再此方法中完成用户登录
        request_data = request.data
        print(request_data)
        return self.list(request, *args, **kwargs)

    def get_student_register(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch_all_patch(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)
