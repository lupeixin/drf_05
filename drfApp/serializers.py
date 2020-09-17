
from rest_framework import serializers, exceptions

# 此序列化器在定义完成后需要使用才生效
from rest_framework.serializers import ModelSerializer

from drfApp.models import Student


class StudentListSerializer(serializers.ListSerializer):
    """
    使用此序列化器完成同时修改多个对象
    """

    # 重写update方法完成批量更新
    def update(self, instance, validated_data):
        # 要修改的对象  要修改的值
        # print(self)     # 当前调用的序列化器类
        # print(instance)  # 要修改的对象
        # print(validated_data)  # 要修改的值

        # 将群改修改成每次修改一个
        for index, obj in enumerate(instance):
            # TODO 每遍历一次 改变一下下标以及对应值和对象
            self.child.update(obj, validated_data[index])

        return instance


class StudentModelSerializer(ModelSerializer):
    """
    序列化器与反序列化器整合
    """

    class Meta:

        # 为修改多个图书提供ListSerializer
        list_serializer_class = StudentListSerializer

        model = Student
        # 指定的字段  填序列化与反序列所需字段并集
        fields = ("stu_name", "age", "gender", "email", "adress")

        # 添加DRF的校验规则  可以通过此参数指定哪些字段只参加序列化  哪些字段只参加反序列化
        extra_kwargs = {
            "stu_name": {
                "max_length": 18,  # 设置当前字段的最大长度
                "min_length": 2,
            }

        }

    # 全局钩子同样适用于 ModelSerializer
    def validate(self, attrs):
        name = attrs.get("stu_name")
        stu = Student.objects.filter(stu_name=name)
        if len(stu) > 0:
            raise exceptions.ValidationError('学生已存在')

        return attrs

    # 局部钩子的使用  验证每个字段
    def validate_age(self, obj):

        # 可以通过self.context获取到视图中传递过来的request对象
        request = self.context.get("request")
        print(request.data)
        # 价格不能超过1000
        if obj > 30:
            raise exceptions.ValidationError("价格最多不能超过30")
        return obj