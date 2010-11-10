from django.db import models
from django.contrib.auth.models import User, Group, Permission

# Create your models here.

class Semester(models.Model) :
	name = models.CharField(max_length=20,primary_key=True)
	start_date = models.DateField()
	end_date = models.DateField()
	reg_start_date = models.DateField()
	reg_end_date = models.DateField()

class Course(models.Model) :
	number = models.SmallIntegerField()
	name = models.CharField(max_length=20)
	dept = models.CharField(max_length=4)
	id = models.IntegerField(primary_key=True)
	prereq = models.ForeignKey('self')
	
class Class(models.Model) :
	class Meta:
		permissions = (("can_teach","is a professor who can teach the course"),)
	semester = models.ForeignKey(Semester)
	days_met = models.CommaSeparatedIntegerField(max_length=5)
	#let's use 0 = Monday, 4 = Friday
	start_time_met = models.DateTimeField() 
	#will ignore the date and just use time
	end_time_met = models.DateTimeField()
	max_class_size = models.IntegerField()
	course = models.ForeignKey(Course)
	professor = models.ForeignKey(User)

class EnrolledClass(models.Model) :
	class Meta :
		permissions = (("can_enroll","is a student who can enroll"),
						("can_set_grades","is allowed to change grades"))
	student = models.ForeignKey(User)
	class_enrolled = models.ForeignKey(Class)
	grade = models.SmallIntegerField()


