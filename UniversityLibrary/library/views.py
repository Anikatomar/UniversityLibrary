from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Book
from .forms import BookForm, StudentForm, BorrowRecordForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm

from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books':books})

@login_required(login_url='login')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save() #Save book in database
            messages.success(request, 'Book added successfully!')
            return redirect('book_list')
    else: #Get request
        form = BookForm()

    return render(request, 'book_form.html',{'form':form})

@login_required(login_url='login')
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('home')
    else:
        form = StudentForm()

    return render(request, 'student_form.html', {'form':form})

@login_required(login_url='login')
def add_borrow_record(request):
    if request.method == 'POST':
        form = BorrowRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Borrow record added successfully!')
            return redirect('home')
    else:
        form = BorrowRecordForm()

    return render(request, 'borrow_form.html', {'form':form})

@login_required(login_url='login')
def edit_book(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book) #instance tells django that form is connected to an existing book, not a new one
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form':form})

@login_required(login_url='login')
def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    return render(request, 'delete_book.html', {'book': book})


# USER REGISTRATION
def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            messages.success(request, 'Registration successful! Please login.')

            return redirect('login')

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

# USER LOGIN
def user_login(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            login(request, user)

            messages.success(request, 'Login successful!')

            return redirect('home')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

# USER LOGOUT
def user_logout(request):

    logout(request)

    messages.success(request, 'You have been logged out.')

    return redirect('home')