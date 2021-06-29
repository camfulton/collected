from django.urls import path

from collection import views

urlpatterns = [
    path('', views.collection_list),
    path('new/global_cards/', views.create_global_cards_collection),
    path('new/global_sets', views.create_global_sets_collection),
    path('new/cards/', views.create_cards_collection),
    path('new/sets/', views.create_sets_collection),
    path('<id>/', views.collection_detail),
]
