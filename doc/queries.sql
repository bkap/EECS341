SELECT * FROM Class WHERE class.professor = professor AND class.semester = semester AND EXISTS (Select * from course where course.id = class.course and course.dept = dept andcourse.number < number)


SELECT * FROM Class WHERE Class.id = class AND EXISTS (SELECT * FROM Semester WHERE Semester.name = Class.semester AND Semester.reg_start_date < today AND Semester.reg_end_date > today) AND NOT EXISTS (SELECT * FROM EnrolledClass WHERE EnrolledClass.class = class.id GROUP BY EnrolledClass.class HAVING Count(*) > Class.max_capacity) AND NOT EXISTS (SELECT * FROM EnrolledClass EC2,Class C2 WHERE EC2.user = user AND C2.id = EC2.class AND C2.semester = Semester.name AND C2.days_met = Class.days_met AND (C2.start_time < Class.start_time AND C2.end_time > Class.start_time) OR (C2.start_time > Class.start_time and C2.start_time < Class.end_time)) AND EXISTS (SELECT * FROM Course where Course.id = Class.course AND (Course.prereq = NULL OR EXISTS (SELECT * From EnrolledClass ec3, Class c3 WHERE ec3.user = user and ec3.class = c3.id AND c3.course = Course.prereq)))

(SELECT * FROM EnrolledClass e,Class c2 WHERE e.user = user AND e.class_enrolled = c2.id AND c2.days = c.days AND ((c2.start_time < c.start_time AND c2.end_time > c.start_time) OR (c2.start_time > c.start_time and c2.start_time < c.end_time)))

