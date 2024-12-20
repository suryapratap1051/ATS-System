from django.contrib import admin
from django.urls import path
from ats.views import analyze_resume

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", analyze_resume, name="analyze_resume"),
]
