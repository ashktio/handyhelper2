from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('jobs/new', views.new_job),
    path('jobs/create', views.create),
    path('<int:job_id>/edit', views.edit_job),
    path('<int:job_id>/update', views.update_job),
    path('<int:job_id>/delete', views.delete_job),
    path('<int:job_id>/details', views.job_profile),
    path('<int:job_id>/<int:user_id>/favorites', views.favorites),
    path('<int:fave_id>/unfavorite', views.unfavorite),
    path('logout', views.logout)
]
