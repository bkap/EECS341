from django.db import models
from django.contrib.auth.models import User, Group, Permission

# Create your models here.

class Semester(models.Model) :
	name = models.CharField(max_length=20,primary_key=True)
	start_date = models.DateField()
	end_date = models.DateField()
	reg_start_date = models.DateField()
	reg_end_date = models.DateField()
	def __str__(self) :
		return self.name
class Room(models.Model) :
	buildingName = models.CharField(max_length=30)
	roomNum = models.IntegerField()
	max_capacity = models.IntegerField()
	class Meta:
		unique_together = (("buildingName","roomNum"),)
	def __str__(self) :
		return "%s %d" % (self.buildingName, self.roomNum)
class Course(models.Model) :
	number = models.SmallIntegerField()
	name = models.CharField(max_length=20)
	dept = models.CharField(max_length=4)
	id = models.IntegerField(primary_key=True)
	prereq = models.ForeignKey('self',null=True,blank=True)
	description = models.TextField(blank=True)
	def __str__(self) :
		return "%s %d: %s" % (self.dept, self.number, self.name)
class Class(models.Model) :
	class Meta:
		permissions = (("can_teach","is a professor who can teach the course"),)
	semester = models.ForeignKey(Semester)
	days_met = models.CommaSeparatedIntegerField(max_length=5)
	#let's use 0 = Monday, 4 = Friday
	start_time_met = models.TimeField() 
	#will ignore the date and just use time
	end_time_met = models.TimeField()
	max_class_size = models.IntegerField()
	course = models.ForeignKey(Course)
	professor = models.ForeignKey(User)
	room = models.ForeignKey(Room)
	def __str__(self) :
		return "Class: %s at %s, %s" % (self.course, self.start_time_met, self.semester)
class EnrolledClass(models.Model) :
	GRADE_CHOICES = (('A','A'),
				('B','B'),
				('C','C',),
				('D','D'),
				('F','F'),
				('S','S'),
				('P','P'),
				('NP','NP'),
				('I','I'))
	class Meta :
		permissions = (("can_enroll","is a student who can enroll"),
						("can_set_grades","is allowed to change grades"))
	student = models.ForeignKey(User)
	class_enrolled = models.ForeignKey(Class)
	grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True,null=True)
	def __str__(self) :
		if self.grade :
			return "%s enrolled in %s with a grade of %s" % (self.student.username, self.class_enrolled, self.grade)
		return "%s enrolled in %s" % (self.student.username, self.class_enrolled)
class Schedule(models.Model) :
	user = models.ForeignKey(User)
	semester = models.ForeignKey(Semester)
	classes_enrolled = models.ManyToManyField(EnrolledClass)
	def __str__(self) :
		return "Schedule for %s in %s" % (self.user, self.semester)
