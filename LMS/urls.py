
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('base',views.BASE,name='base'),
    path('404',views.PAGE_NOT_FOUND,name="404"),
    path('',views.home,name='home'),
    path('courses',views.single_course,name='single_course'),
    path('course/filter-data',views.filter_data,name="filter-data"),
    path('course/<slug:slug>',views.COURSE_DETAILS,name='course_details'),
    path('search',views.Search_Course,name='search_course'),
    path('contact_us',views.contact_us,name='contact_us'),
    path('about_us',views.about_us,name='about_us'),
    path('login/', views.login, name='login'),
    path('singin',views.singin,name='singin'),
    path('register',views.register,name='register'),
    path('do_login', views.do_login, name='do_login'),
    path('logout/', views.logout, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('profile',views.Profile,name='profile'),
    path('profile/update',views.profile_update,name='profile_update'),
    path('checkout/<slug:slug>',views.checkout,name='checkout'),
    path('my-course',views.MY_COURSE,name='my_course'),
    path('verify_payment',views.VERIFY_PAYMENT,name='verify_payment'),






 ]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)










