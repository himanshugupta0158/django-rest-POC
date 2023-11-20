from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
# router.register(r'generate_users', views.Generate_Random_Users)

urlpatterns = [
    path('', include(router.urls)),
    path('generate_users/', views.Generate_Random_Users.as_view()),
    path('search/<key>/', views.SearchUser.as_view()),
    
    # GenericAPIView - Default , CRUD
    path('student_list/', views.StudentList.as_view()),
    path('student_list/<pk>/', views.StudentList.as_view()),

    # Generic API View + DRF Mixins - Default , CRUD
    path('student-view/', views.StudentView.as_view()),
    path('student-view/<pk>/', views.StudentDetailView.as_view()), # pk is used as default if anything is not given by user

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
]
