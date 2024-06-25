from django.urls import path
from .views import HomeView, RoomView, SendMessageView, LoginView, SignupView

urlpatterns = [
    path('', HomeView, name='home'),
    path('room/<str:room_name>/<str:username>/', RoomView, name='room'),
    path('send/<str:room_name>/', SendMessageView, name='send_message'),
    path('login/', LoginView, name='login'),
    path('signup/', SignupView, name='signup'),
]