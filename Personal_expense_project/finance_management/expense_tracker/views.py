from datetime import datetime, timedelta

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage,InvalidPage
from django.shortcuts import  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Expens
from .forms import ExpenseForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import LoginForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log in the user
                login(request, user)
                return redirect('view_expenses')
            else:
                # Invalid login credentials
                messages.error(request, 'Invalid login credentials.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class ExpenseCreateView(View):
    template_name = 'expense_create.html'

    def get(self, request):
        form = ExpenseForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.created_by = User.objects.get(email=request.user.email)
            expense.save()
            messages.success(request, 'Expense created successfully!')
            return redirect('view_expenses')
        else:
            messages.error(request, 'Expense create request failed.')
            return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name='dispatch')
class ExpenseListView(View):
    template_name = 'expense_list.html'
    items_per_page = 7
    def get(self, request):

        date_filter = request.GET.get('date_filter', '')
        name_search = request.GET.get('name_search', '')

        if request.user.is_staff:
            expenses = Expens.objects.all()
        else:
            expenses = Expens.objects.filter(created_by=request.user)
        print(request.user)
        print(f"Date Filter: {date_filter}")
        print(f"Name Search: {name_search}")
        print(f"Filtered Expenses: {expenses}")
        # Filter by Date
        if date_filter:
            try:
                # Parse the date filter value
                selected_date = datetime.strptime(date_filter, "%Y-%m-%d").date()
                print(selected_date)
                # Adjust the range as needed
                start_date = selected_date
                end_date = selected_date + timedelta(days=0)

                # Filter expenses based on the date range
                expenses = Expens.objects.filter(date__range=[start_date, end_date])
            except ValueError:
                # Handle invalid date format gracefully
                expenses = Expens.objects.all()
        # else:
        #     # If no date filter is provided, display all expenses
        #     expenses = Expens.objects.all()



        # Search by Expense Name
        if name_search:
            expenses = expenses.filter(name__icontains  =name_search)

        # pagination
        paginator = Paginator(expenses, self.items_per_page)
        page = request.GET.get('page')
        try:
            expenses = paginator.page(page)
        except PageNotAnInteger:
            expenses = paginator.page(1)
        except EmptyPage:
            expenses = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'expenses': expenses})

@method_decorator(login_required, name='dispatch')
class ExpenseEditView(View):
    template_name = 'expense_edit.html'

    def get(self, request, expense_id):
        expense = get_object_or_404(Expens, id=expense_id, created_by=request.user)
        if not request.user.is_staff and expense.created_by != request.user:
            messages.error(request, 'You do not have permission to edit this expense.')
            return redirect('view_expenses')
        form = ExpenseForm(instance=expense)
        return render(request, self.template_name, {'form': form, 'expense': expense})

    def post(self, request, expense_id):
        expense = get_object_or_404(Expens, id=expense_id, created_by=request.user)
        if not request.user.is_staff and expense.created_by != request.user:
            messages.error(request, 'You do not have permission to edit this expense.')
            return redirect('view_expenses')
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('view_expenses')
        else:
            messages.error(request, 'Expense update request failed.')
            return render(request, self.template_name, {'form': form, 'expense': expense})

@method_decorator(login_required, name='dispatch')
class ExpenseDeleteView(View):
    template_name = 'expense_delete.html'

    def get(self, request, expense_id):
        expense = get_object_or_404(Expens, id=expense_id, created_by=request.user)
        return render(request, self.template_name, {'expense': expense})

    def post(self, request, expense_id):
        expense = get_object_or_404(Expens, id=expense_id, created_by=request.user)
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('view_expenses')


