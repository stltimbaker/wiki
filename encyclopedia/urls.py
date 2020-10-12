from django.urls import path

from . import views

#app_name = 'wiki'
urlpatterns = [
    # /wiki/
    path("", views.index, name="index"), 

    # /wiki/TITLE
    path("<str:title>/", views.detail, name="detail"),

    # /wiki/search
    path("search", views.search, name="search"), 

    # /wiki/add
    path("add", views.add, name="add"),

    # /wiki/TITLE
    path("random", views.random, name="random"),

    # /wiki/editentry
    path("editentry/<str:id>", views.editentry, name="editentry")
]
