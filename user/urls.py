from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('login/', views.loginPage, name="login"),
	path('register/', views.registerPage, name="register"),
	path('logout/', views.logoutUser, name="logout"),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="base/password_reset.html"), name="password_reset"),

    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name="base/email_sent.html"),name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html",),
                                                                                          name="password_reset_confirm"),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="base/password_reset_complete.html"), name="password_reset_complete"),


    #path('account/', views.userAccount, name="account"),
    #path('profile/', views.profile, name='profile'),
    path('update_profile/', views.updateProfile, name="update_profile"),

]
