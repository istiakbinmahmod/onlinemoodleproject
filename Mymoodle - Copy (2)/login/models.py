"""
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_id = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=20)
    email_id = models.EmailField()
    name = models.CharField(max_length=30)
    date_of_birth = models.DateField()


    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "PROFILE"

class CourseSession(models.Model):
    course_id = models.CharField(max_length=20, primary_key=True)
    session_id = models.CharField(max_length=20)
    course_title = models.CharField(max_length=100)
    credit_hour = models.IntegerField()
    class Meta:
        db_table = "COURSE"


"""
