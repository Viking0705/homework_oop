class Student:
    list_students = []
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        Student.list_students.append(self)
    
    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'
        
    def __average_grade(self):
        sum_grades = 0
        len_grades = 0
        for grades in self.grades.values():
            sum_grades += sum(grades)
            len_grades += len(grades)
        return sum_grades / len_grades
    
    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {self.__average_grade():.2f}\nКурсы в процессе изучения: {", ".join(self.courses_in_progress)}\nЗавершенные курсы: {", ".join(self.finished_courses)}'
        return res

    def __lt__(self, other_student):
        if not isinstance(other_student, Student):
            print('Not a Student')
            return
        return self.__average_grade() < other_student.__average_grade()
        
class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

class Lecturer(Mentor):
    list_lecturers = []
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
        Lecturer.list_lecturers.append(self)
    
    def __average_grade(self):
        sum_grades = 0
        len_grades = 0
        for grades in self.grades.values():
            sum_grades += sum(grades)
            len_grades += len(grades)
        return sum_grades / len_grades
    
    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.__average_grade():.2f}'
        return res
    
    def __lt__(self, other_lecturer):
        if not isinstance(other_lecturer, Lecturer):
            print('Not a Lecturer')
            return
        return self.__average_grade() < other_lecturer.__average_grade()        

class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'
        
    def __str__(self):
        res = f'Имя: {self.name}\nФамилия: {self.surname}'
        return res



def average_grade_students_in_course(list_students, course_name):
    len_grade = 0
    sum_grade = 0
    for student in list_students:
        if course_name in student.courses_in_progress and student.grades.get(course_name):
            sum_grade += sum(student.grades[course_name])
            len_grade += len(student.grades[course_name])
    return f'{sum_grade / len_grade:.2f}' if len_grade else f"такой курс не изучает ни один студент"

def average_grade_lecturers_in_course(list_lecturers, course_name):
    len_grade = 0
    sum_grade = 0
    for lecturer in list_lecturers:
        if course_name in lecturer.courses_attached and lecturer.grades.get(course_name):
            sum_grade += sum(lecturer.grades[course_name])
            len_grade += len(lecturer.grades[course_name])
    return f'{sum_grade / len_grade:.2f}' if len_grade else f"такой курс не преподает ни один лектор"


student1 = Student('Анна', 'Смирнова', 'жен.')
student1.courses_in_progress += ['Python']
student1.courses_in_progress += ['Git']
student1.finished_courses += ['Введение в программирование']
student1.finished_courses += ['C++']
student1.grades['Git'] = [5, 7]
student1.grades['Python'] = [9, 10]
student2 = Student('Елена', 'Серегина', 'жен.')
student2.courses_in_progress += ['Python', 'Git', 'C++']
student2.grades['Python'] = [3, 6, 3]
student2.grades['C++'] = [10]
 
lecturer1 = Lecturer('Иван', 'Иванов')
lecturer1.courses_attached += ['Python']
lecturer1.courses_attached += ['Git']
lecturer2 = Lecturer('Боб', 'Бобов')
lecturer2.courses_attached += ['Git', 'C++']

reviewer1 = Reviewer('Петр','Петров')
reviewer1.courses_attached += ['Git']
reviewer2 = Reviewer('Николай','Николаев')
reviewer2.courses_attached += ['Python']

print('***')
print(f'     Справочная информация.')
print(f' Студенты.')
print(f'Изучаемые курсы Анны Смирновой(st1): {", ".join(student1.courses_in_progress)}')
print(f'Изначальные оценки по изучаемым курсам Анны Смирновой(st1): {student1.grades}')
print(f'Изучаемые курсы Елены Серегиной(st2): {", ".join(student2.courses_in_progress)}')
print(f'Изначальные оценки по изучаемым курсам Елены Серегиной(st2): {student2.grades}')
print(f' Лекторы.')
print(f'Иван Иванов (lec1) – лектор по {", ".join(lecturer1.courses_attached)}')
print(f'Боб Бобов (lec2) – лектор по {", ".join(lecturer2.courses_attached)}')
print(f' Проверяющие.')
print(f'Петр Петров (rev1) – лектор по {", ".join(reviewer1.courses_attached)}')
print(f'Николай Николаев (rev2) – лектор по {", ".join(reviewer2.courses_attached)}')
print('\n***')

print('     Проверяющие оценивают студентов.')
reviewer1.rate_hw(student1,'Git', 10)
print(f'Rev1 оценил st1 по Git на 10.\nНовые оценки st1: {student1.grades}\n')
reviewer2.rate_hw(student2,'Python', 7)
print(f'Rev2 оценил st2 по Python на 7.\nНовые оценки st2: {student2.grades}\n')
reviewer1.rate_hw(student1,'Python', 3)
print(f'Rev1 пытается оценить st1 по Python на 3, где не является проверяющим.\nОценки st1 не меняются: {student1.grades}\n')
reviewer2.rate_hw(student1,'C++', 5)
print(f'Rev2 пытается оценить st1 по C++ на 5, но st1 не изучает сейчас C++.\nОценки st1 не меняются: {student1.grades}\n')
reviewer1.rate_hw(student2,'Git', 8)
print(f'Rev1 оценил st2 по Git на 8.\nНовые оценки st2: {student2.grades}\n')
print('\n***')

print('     Студенты оценивают лекторов.')
student1.rate_lecturer(lecturer1, 'Python', 10)
student1.rate_lecturer(lecturer1, 'Python', 9)
student1.rate_lecturer(lecturer1, 'Python', 10)
print(f'St1 оценил lec1 по Python на 10, 9, 10.\nНовые оценки lec1: {lecturer1.grades}\n')
student1.rate_lecturer(lecturer1, 'Git', 8)
student1.rate_lecturer(lecturer1, 'Git', 7)
print(f'St1 оценил lec1 по Git на 8, 7.\nНовые оценки lec1: {lecturer1.grades}\n')
student1.rate_lecturer(lecturer2, 'C++', 4)
print(f'St1 пытается оценить lec2 по С++ на 4, но st1 не изучает сейчас C++.\nОценки lec1 не меняются: {lecturer1.grades}\n')
student2.rate_lecturer(lecturer2, 'C++', 4)
student2.rate_lecturer(lecturer2, 'C++', 6)
student2.rate_lecturer(lecturer2, 'C++', 8)
print(f'St2 оценил lec2 по C++ на 4, 6, 8.\nНовые оценки lec2: {lecturer2.grades}\n')
student2.rate_lecturer(lecturer1, 'C++', 5)
print(f'St2 пытается оценить lec1 по С++ на 5, но lec1 не является лектором по C++.\nОценки lec1 не меняются: {lecturer1.grades}\n')
student2.rate_lecturer(lecturer2, 'Git', 9)
print(f'St2 оценил lec2 по Git на 9.\nНовые оценки lec2: {lecturer2.grades}\n')
student2.rate_lecturer(lecturer1, 'Python', 6)
print(f'St2 оценил lec1 по Python на 6.\nНовые оценки lec1: {lecturer1.grades}\n')
print('\n***')

print('     Справочная информация.')
print(f'Оценки студента Анны Смирновой (st1): {student1.grades}')
print(f'Оценки студента Елены Серегиной (st2): {student2.grades}')
print(f'Оценки лектора Ивана Иванова (lec1): {lecturer1.grades}')
print(f'Оценки лектора Боба Бобова (lec2): {lecturer2.grades}')
print('\n***')
 
print(f"    Выводим данные проверяющих.")
print(reviewer1)
print(reviewer2)
print(f"\n   Выводим данные лекторов.")
print(lecturer1)
print(lecturer2)
print(f"\n  Сравниваем лекторов по средней оценке.\n{lecturer1.name} {lecturer1.surname} > {lecturer2.name} {lecturer2.surname}? --- {lecturer1 > lecturer2}")
print(f"\n   Выводим данные студентов.")
print(student1)
print(student2)
print(f"\n   Сравниваем студентов по средней оценке.\n{student1.name} {student1.surname} < {student2.name} {student2.surname}? --- {student1 < student2}")

print(f"\n   Средняя оценка студентов курсов.")
print(f"Средняя оценка студентов курса Python: {average_grade_students_in_course(Student.list_students, 'Python')}")
print(f"Средняя оценка студентов курса Git: {average_grade_students_in_course(Student.list_students, 'Git')}")
print(f"Средняя оценка студентов курса C++: {average_grade_students_in_course(Student.list_students, 'C++')}")
print(f"Средняя оценка студентов курса C#: {average_grade_students_in_course(Student.list_students, 'C#')}")

print("\n   Средняя оценка лекторов курсов.")
print(f"Средняя оценка лекторов курса Python: {average_grade_lecturers_in_course(Lecturer.list_lecturers, 'Python')}")
print(f"Средняя оценка лекторов курса Git: {average_grade_lecturers_in_course(Lecturer.list_lecturers, 'Git')}")
print(f"Средняя оценка лекторов курса C++: {average_grade_lecturers_in_course(Lecturer.list_lecturers, 'C++')}")
print(f"Средняя оценка лекторов курса C#: {average_grade_lecturers_in_course(Lecturer.list_lecturers, 'C#')}")