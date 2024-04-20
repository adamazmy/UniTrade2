from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.account, name='account'),
    path('current/', views.current, name='current'),
    path('marketplace/<int:product_id>/', views.viewItem, name='item'),
    path('remove_item/<int:product_id>/', views.remove_item, name='remove_item'),
    path('add_comment/<int:product_id>/', views.add_comment, name='add_comment'),
    path('add/', views.addItem, name='add'),
    path('<int:product_id>/edit/', views.edit_item, name='edit'),
    path('condition/', views.inputCondition, name='condition'),
    path('',views.productPage, name= 'products'),
    path('aboutus/', views.aboutUs, name= 'aboutus'),
    path('faq/', views.faq, name= 'faq'),
    path('department/books/', views.books, name= 'books'),
    path('department/technology/', views.technology, name= 'technology'),
    path('department/sportsleisure/', views.sportsLeisure, name= 'sportsleisure'),
    path('department/electroniccomputers/', views.electronicsComputer, name= 'electroniccomputers'),
    path('department/education/', views.education, name= 'education'),
    path('department/homeEquipment/', views.homeEquipment, name= 'homeEquipment'),
    path('department/filmTvMusic/', views.filmTvMusic, name= 'filmTvMusic'),
    path('search/', views.search_action, name='search_view'),
    path('termsandconditions/', views.termsandcond, name='termsandconditions'),
    path('privacypolicy/', views.privacypolicy, name='privacypolicy'),
    
    

]