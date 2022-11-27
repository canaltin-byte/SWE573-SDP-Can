from django.db import models

# çöp
class Category(models.Model):
    user_id = models.IntegerField(max_length=30)
    category_names = models.CharField(max_length=1000)


try:
    student = models.Student.objects.get(name="abc")
except:
    student = None
    students = models.Student.objects.filter(name="abc")

if student:
    print(student.id)
else:
    if students:
        print("There are multiple users with this name")
    else:
        print("The user doesn't exist")
