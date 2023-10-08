from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("" , views.index, name="ShopHome"),
    path("about/",views.about,name="AboutUs"),
    path("contact/",views.contact,name="ContactUs"),
    path("tracker/",views.tracker,name="TrackingStatus"),
    path("search/",views.search,name="Search"),
    path("productview/<int:id>",views.productview,name="productview"),
    path("checkout/",views.checkout,name="Checkout"),
    path('payment/', views.payment, name='payment'),
    path('success/',views.success,name="success")
]
