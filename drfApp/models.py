from django.db import models


# Create your models here.
class Student(models.Model):
    gender_choices = (
        (0, "male"),
        (1, "female"),
        (2, "other"),
    )

    stu_name = models.CharField(max_length=60)
    age = models.CharField(max_length=64)
    class_name = models.ForeignKey(to="Class", on_delete=models.CASCADE, db_constraint=False, related_name="cla_name")
    gender = models.SmallIntegerField(choices=gender_choices, default=0)
    mail = models.CharField(max_length=80, default="xxxxxxx@qq.com")
    adress = models.CharField(max_length=11)

    class Meta:
        db_table = 'students'
        verbose_name = "学生"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.stu_name


class Class(models.Model):
    class_name = models.CharField(max_length=60)
    class_num = models.CharField(max_length=80)
    class_cate = models.CharField(max_length=80)

    class Meta:
        db_table = 'Class'
        verbose_name = "班级"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.class_name