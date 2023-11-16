from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
# router.register(r'generate_users', views.Generate_Random_Users)

urlpatterns = [
    path('', include(router.urls)),
    path('generate_users', views.Generate_Random_Users.as_view()),
    path('search/<key>', views.SearchUser.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
]
