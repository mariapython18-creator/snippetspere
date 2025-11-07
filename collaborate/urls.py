"""
URL configuration for developer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from collaborate import views
app_name='collaborate'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('experts/', views.Experts.as_view(), name='experts'),
    path('collab/', views.Collab.as_view(), name='collab'),
    path('sender_dashboard/', views.SenderDashboardView.as_view(), name='sender_dashboard'),
    path('discussion/<int:id>', views.DiscussionView.as_view(), name='discussion'),
    path('expertslist/', views.Expertslist.as_view(), name='expertslist'),

]
