from . import views
from django.urls import path
from .views import ExpenseCreateView,ExpenseListView,ExpenseEditView,ExpenseDeleteView
from django.contrib.auth.views import LoginView

urlpatterns=[

    path('',views.login_view , name='login'),
    path('create/',ExpenseCreateView.as_view(),name='create_expense'),
    path('view/',ExpenseListView.as_view(),name='view_expenses'),
    path('edit/<int:expense_id>/',ExpenseEditView.as_view(),name='edit_expense'),
    path('delete/<int:expense_id>/',ExpenseDeleteView.as_view(),name='delete_expense'),
]