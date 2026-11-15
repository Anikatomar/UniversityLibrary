from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    country = models.CharField(max_length = 50)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length = 20)
    price = models.DecimalField(max_digits = 8, decimal_places = 2)
    published_year = models.IntegerField()

    author = models.ForeignKey(Author,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20)
    email = models.EmailField()
    branch = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class BorrowRecord(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete = models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.student} - {self.book}"
