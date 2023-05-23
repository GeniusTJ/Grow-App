from django.urls import path

from . import views
app_name= "projects"
urlpatterns =[
   
    path('', views.project_list_view.as_view(),name='feed'),
    path('<int:project_id>/details/',views.details,name='details'),
    path('<int:project_id>/makeSubmission/',views.make_submission,name='make_submission'),
    path('createProject/',views.create_project_form,name='create_project_form'),
    path('create/',views.create_project,name='create_project'),
    path('<int:project_id>/setranks/',views.set_ranks,name='set_ranks')
    
]
