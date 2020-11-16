from django.urls import path, include
from rest_framework import routers

from question_manager import views
from question_manager.views import OrganizationViewSet, DepartmentViewSet

router = routers.DefaultRouter()
router.register(r'organization', OrganizationViewSet)
router.register(r'department', DepartmentViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path("user-organizations/", views.UserOrganizationsView.as_view()),

    path("departments/<str:organization>/", views.OrganizationsDepartmentsView.as_view()),

    path("categories/<str:organization>/<str:department>/<int:pk>/", views.CategoriesView.as_view()),
    path("categories/<str:organization>/<str:department>/", views.CategoriesView.as_view()),
    path("category/<str:organization>/<str:department>/<int:pk>/", views.CategoryView.as_view()),
    path("category/<str:organization>/<str:department>/", views.CategoryView.as_view()),

    path("questions/<str:organization>/<str:department>/<int:category_id>/", views.QuestionsView.as_view()),
    path("question/<str:organization>/<str:department>/<int:pk>/", views.QuestionView.as_view()),
    path("question/<str:organization>/<str:department>/", views.QuestionView.as_view()),

    path("chat-bots/<str:organization>/", views.ChatBotsView.as_view()),
    path("chat-bot/<str:organization>/<int:pk>/", views.ChatBotView.as_view()),
    path("chat-bot/<str:organization>/", views.ChatBotView.as_view()),
]
