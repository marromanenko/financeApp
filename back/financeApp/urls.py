from django.urls import path, include
from rest_framework import routers
from . import views
router = routers.DefaultRouter()
router.register(r'users', views.CustomUserViewSet)
router.register(r'transports', views.TransportViewSet)
router.register(r'accomodations', views.AccomodationViewSet)

urlpatterns = [
    path("login/", views.UserLoginAPIView.as_view(), name="user_login"),
    path("register/", views.UserRegisterAPIView().as_view(), name="user_register"),
    path("logout/", views.UserLogoutAPIView.as_view(), name="user_logout"),
    path('api/description/', views.DescriptionView.as_view(), name='about_info'),
    path('api/profile/', views.ProfileView.as_view(), name='profile_info'),
    path('api/compute', views.ComputeView.as_view(), name='compute'),
    path('api/', include(router.urls)),
]


