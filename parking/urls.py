from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name="index"),
	path('parking', views.goingIn, name="entrada"),
	path('pay', views.payment, name="pagamento"),
]