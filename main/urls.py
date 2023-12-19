from.import views
from django.urls import path,include

app_name = 'main'

urlpatterns=[
    path('',views.index,name='index'),
    
    path('component_City/',views.component_City,name='component_City'),
    path('component_Country/',views.component_Country,name='component_Country'),
    path('component_Intensity/',views.component_Intensity,name='component_Intensity'),
    path('component_Region/',views.component_Region,name='component_Region'),
    path('component_Year/',views.component_Year,name='component_Year'),

]