from django import forms
from datetime import date
from .models import Book,Student, BorrowRecord

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'price', 'published_year', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'published_year': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean_isbn(self):
        isbn = self.cleaned_data['isbn']

        # Allow the existing ISBN when editing the same book,
        # but prevent duplicates for other books.
        qs = Book.objects.filter(isbn=isbn)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "A book with this ISBN already exists."
            )

        return isbn
    def clean_price(self):
        price = self.cleaned_data['price']

        if price <= 0:
            raise forms.ValidationError(
                "Price must be greater than zero."
            )

        return price
    def clean_published_year(self):
        year = self.cleaned_data['published_year']

        if year < 1000 or year > date.today().year:
            raise forms.ValidationError(
                "Enter a valid published year."
            )

        return year

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_no', 'email', 'branch']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'roll_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'branch': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_roll_no(self):
        roll_no = self.cleaned_data['roll_no']
        qs = Student.objects.filter(roll_no=roll_no)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "A student with this roll number already exists."
            )

        return roll_no

class BorrowRecordForm(forms.ModelForm):
    class Meta:
        model = BorrowRecord
        fields = [
            'student', 'book', 'borrow_date',
            'return_date', 'status'
        ]

        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'book': forms.Select(attrs={'class': 'form-control'}),
            'borrow_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'return_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        borrow_date = cleaned_data.get('borrow_date')
        return_date = cleaned_data.get('return_date')

        if borrow_date and return_date and return_date < borrow_date:
            self.add_error(
                'return_date',
                "Return date cannot be earlier than borrow date."
            )

        return cleaned_data

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")

        return username

