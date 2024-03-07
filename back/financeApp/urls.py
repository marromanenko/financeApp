from django.urls import path, include
from rest_framework import routers
#
from . import views
# from views import UserLoginAPIView
# from views import UserRegisterAPIView
# from views import UserLogoutAPIView

#
router = routers.DefaultRouter()
router.register(r'users', views.CustomUserViewSet)
router.register(r'transports', views.TransportViewSet)
router.register(r'accomodations', views.AccomodationViewSet)
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#     path('', include(router.urls)),
# ]
#
# urlpatterns += router.urls


# from views import UserLoginAPIView
# from views import UserRegisterAPIView
# from views import UserLogoutAPIView
urlpatterns = [
    path("login/", views.UserLoginAPIView.as_view(), name="user_login"),
    path("register/", views.UserRegisterAPIView().as_view(), name="user_register"),
    path("logout/", views.UserLogoutAPIView.as_view(), name="user_logout"),
    path('api/', include(router.urls)),
]


