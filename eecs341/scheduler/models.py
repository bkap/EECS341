from django.db import models

# Create your models here.
class User(models.Model) :
	name = models.CharField(max_length=60)
	ROLE_CHOICES = ( ('S','student'),
					 ('P','proessor'),
					 ('A','administrator') )
	role = models.CharField(max_length=1,choices=ROLE_CHOICES)

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
	semester = models.ForeignKey(Semester)
	days_met = models.CommaSeparatedIntegerField(max_length=5)
	#let's use 0 = Monday, 4 = Friday
	start_time_met = models.DateTimeField() 
	#will ignore the date and just use time
	end_time_met = models.DateTimeField()
	max_class_size = models.IntegerField()
	students = models.ManyToManyField(User)
	course = models.ForeignKey(Course)

