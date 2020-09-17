from django.urls import path

from drfApp import views

urlpatterns = [
    path("student/", views.StudentAPIView.as_view()),
    path("student/<str:id>/", views.StudentAPIView.as_view()),
    path("gen/", views.StudentGenericAPIView.as_view()),
    path("gen/<str:id>/", views.StudentGenericAPIView.as_view()),

    path("mix/", views.StudentGenericMixinView.as_view()),
    path("mix/<str:id>/", views.StudentGenericMixinView.as_view()),

    path("set/", views.StudentModelViewSet.as_view({"post": "student_login", "get": "get_student_register", "patch": "patch_all_patch"})),
    path("set/<str:id>/", views.StudentModelViewSet.as_view({"post": "student_login", "get": "get_student_register", "patch": "patch_all_patch"})),
]
