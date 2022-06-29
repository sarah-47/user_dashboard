from django.urls import path
from . import views
#urlpatterns => static name
urlpatterns = [
# mapping '/' to index function in views file
path('', views.index),
path('register', views.register),
path('signin', views.signin),
path('dashboard/admin', views.dashboard),
path('logoff', views.logoff),
path('editUser/<int:userId>',views.editUser),
path('removeUser/<int:userId>',views.removeUser),
path('users/new',views.addUser),
path('dashboard/users', views.userDshboard),
path('users/edit/<int:userId>', views.userEdit),
path('userEditPassword/<int:userId>', views.userEditPassword),
path('userEditDesc/<int:userId>', views.userEditDesc),
path('users/Adminedit/<int:userId>', views.Adminedit),
path('adminEditPassword/<int:userId>', views.adminEditPassword),

path('users/show/<int:id>', views.show_user),
path('post_message/<int:id>',views.post_message),
path('post_comment/<int:id>',views.post_comment),


]
#12@Hh6453
