from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'students', views.StudentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('generate_users/', views.Generate_Random_Users.as_view()),
    path('search/<key>/', views.SearchUser.as_view()),
    path('search_with_filters/<key>/', views.SearchUserWithPaginationAndFilters.as_view()),
    
    # GenericAPIView - Default , CRUD
    path('student_list/', views.StudentList.as_view()),
    path('student_list/<pk>/', views.StudentList.as_view()),

    # Generic API View + DRF Mixins - Default , CRUD
    path('student-view/', views.StudentView.as_view()),
    path('student-view/<pk>/', views.StudentDetailView.as_view()), # pk is used as default if anything is not given by user

    # viewsets.ModelViewset APIs with filters and Search below as well as CRUD API via routers of rest_framework
    path('students/search/<str:name>/', views.StudentViewSet.as_view({'get': 'search_by_name'}), name='search-by-name'),
    path('students/filter/passby/<str:passby>/', views.StudentViewSet.as_view({'get': 'filter_by_passby'}), name='filter-by-passby'),
    path('students/sort/<str:field>/', views.StudentViewSet.as_view({'get': 'sort_students'}), name='sort_students'),
    path('students/group/<str:field>/', views.StudentViewSet.as_view({'get': 'group_students'}), name='group_students'),
    path('students/distinct/<str:field>/', views.StudentViewSet.as_view({'get': 'distinct_values'}), name='distinct_values'),
    path('students/recent/<int:count>/', views.StudentViewSet.as_view({'get': 'recent_students'}), name='recent_students'),
    path('students/query/total-count/', views.StudentViewSet.as_view({'get': 'total_students_count'}), name='total_students_count'),
    path('students/query/random/', views.StudentViewSet.as_view({'get': 'random_student'}), name='random_student'),
    path('students/query/statistics/', views.StudentViewSet.as_view({'get': 'student_statistics'}), name='student_statistics'),
    path('students/query/pass-percentage/', views.StudentViewSet.as_view({'get': 'pass_percentage'}), name='pass_percentage'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
]
