from django.urls import path, include
from rest_framework import routers

from question_manager import views
from question_manager.views import OrganizationViewSet

router = routers.DefaultRouter()
router.register(r'organization', OrganizationViewSet)

urlpatterns = [
    path("organizations/", views.UserOrganizationsView.as_view()),
    path('', include(router.urls)),

    path("categories/<str:organization>/<str:department>/<int:pk>/", views.CategoriesView.as_view()),
    path("categories/<str:organization>/<str:department>/", views.CategoriesView.as_view()),
    path("category/<str:organization>/<str:department>/<int:pk>/", views.CategoryView.as_view()),

    path("questions/<str:organization>/<str:department>/<int:category_id>/", views.QuestionsView.as_view()),
    path("questions/<str:organization>/<str:department>/", views.QuestionsView.as_view()),
    path("question/<str:organization>/<str:department>/<int:pk>/", views.QuestionView.as_view()),

]
