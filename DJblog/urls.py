from django.urls import path
from .views import post_list , post_detail , post_new , post_edit , post_delete

urlpatterns = [
    path('',post_list),
    path('<int:post_id>',post_detail),
    path('new',post_new),
    path('<int:post_id>/edit',post_edit),
    path('<int:post_id>/delete',post_delete),
]
