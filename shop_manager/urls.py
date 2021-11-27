"""shop_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',views.home),
    path('customer_info/',views.customer_info),
    path('bill/',views.bill),
    path('bill_receipt/',views.bill_receipt),
    path('inventory1/',views.inventory1),
    path('inventory2/',views.inventory2),
    path('item_detail1/',views.item_detail1),
    path('allbills/',views.showbill),
    path('salesgst/',views.salesgst),
    path('gstcollection/',views.gstdict),
    path('dailysale/',views.dailysale)]
