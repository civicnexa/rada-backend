from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register('services', views.ServiceView, basename='services')
router.register('projects', views.ProjectsView, basename='projects')
router.register('testimonial', views.TestimonialView, basename='testimonial')
router.register('contactus', views.ContactUsView, basename='contactus')
router.register('subservices', views.SubServiceView, basename='subservices')
router.register('teams', views.TeamView, basename='teams')
router.register('clients', views.ClientsView, basename='clients')

urlpatterns = [
    # path('contactus/', views.SubmitContactUsView.as_view(), name='contactus'),
    path('homedata/', views.HomeData.as_view(), name='homedata'),
    path('aboutus/', views.AboutUsPageView.as_view(), name='aboutus'),
    path('downloadcontact/', views.ExportContactCSVView.as_view(), name='contactdownload'),
]

urlpatterns += router.urls
