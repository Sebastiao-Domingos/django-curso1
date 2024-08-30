from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Author(BaseModel):
    name = models.CharField(max_length=240)
    date_of_birth = models.DateField()
    date_of_death = models.DateField(null=True , blank=True)
    books = models.ManyToManyField("Book" , related_name="authors")

    class Meta :
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
    
    def __str__(self) -> str:
        return self.name
    

    def get_absolute_url(self):
        return reverse("author-detail", kwargs={"pk": self.pk})
    
    
class Genre(BaseModel):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField("Book" , related_name="genres")
    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self) -> str:
        return self.name    


class Language(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'
        ordering =   ["name"]

    def __str__(self):
        return self.name
    

class BookInstance(BaseModel):
    LOAN_STATUS = (("d" , "disponivel" , ) , ("m" , "manutenção") , ("r" , "reservado" ) , ("o" , "em empréstimo"))
    id = models.UUIDField(primary_key=True , default= uuid.uuid4() , help_text="Enter with unique code indentifier")
    imprint = models.CharField(max_length=250)
    due_back = models.DateTimeField()
    status  = models.CharField(max_length=1 , choices= LOAN_STATUS , default="m")
    books = models.ForeignKey("Book" , on_delete=models.SET_NULL, null=True )
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        # Get the current time as a timezone-aware datetime
        now = timezone.now()

        # Ensure due_date is also timezone-aware
        if timezone.is_naive(self.due_back):
            self.due_back = timezone.make_aware(self.due_back, timezone.get_current_timezone())

        # Compare the two timezone-aware datetime objects
        return now > self.due_back


    class Meta :
        verbose_name = 'Book Instance'
        verbose_name_plural = 'Book Instances'
        ordering = ["created_at", "updated_at"]

    def __str__(self):
        return self.status


class Book(BaseModel):
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=250)
    ISBN = models.CharField(max_length=100)
    language = models.ForeignKey(Language , on_delete=models.SET_NULL , null=True)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['title']

    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse("book-detail", kwargs={"pk": self.pk})
    
    

    
    