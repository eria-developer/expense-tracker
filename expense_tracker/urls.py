from django.contrib import admin
from django.urls import path, include
from expenses import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("expenses/", include("expenses.urls"))
]
