from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('dashboard', views.display_dashboard),
    path('register', views.register_user),
    path('submit', views.jobs),
    path('edit/<int:job_id>', views.update_job),
    path('login', views.login_user),
    path('logout', views.logout_user),
    path('jobs/new', views.new_job),
    path('jobs/<int:job_id>', views.jobs_int),
    path('jobs/edit/<int:job_id>', views.job_render),
    path('jobs/remove/<int:job_id>', views.delete_job)

]