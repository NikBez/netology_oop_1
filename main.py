from numpy import average


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lection(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer)
                and course in self.courses_in_progress
                and course in lecturer.courses_attached
                and grade in range(11)):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def get_average_grade(self):
        if self.grades:
            return average(list(self.grades.values()))
        else:
            return 0

    def __str__(self):
        avg_grade = self.get_average_grade()
        courses_in_progress = ', '.join(self.courses_in_progress) or 'Нет'
        finished_courses = ', '.join(self.finished_courses) or 'Нет'
        return f'''
        Имя: {self.name}
        Фамилия: {self.surname}
        Средняя оценка за домашние задания: {avg_grade}
        Курсы в процессе изучения: {courses_in_progress}
        Завершенные курсы: {finished_courses}
        '''

    def __lt__(self, another_student):
        if isinstance(another_student, Student):
            return self.get_average_grade() < another_student.get_average_grade()
        else:
            return 'Ошибка. Сравнивать можно только с другим студентом'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def get_average_grade(self):
        if self.grades:
            return average(list(self.grades.values()))
        else:
            return 0

    def __str__(self):
        avg_grade = self.get_average_grade()
        return f'''
        Имя: {self.name}
        Фамилия: {self.surname}
        Средняя оценка за лекции: {avg_grade}
        '''

    def __lt__(self, another_lecturer):
        if isinstance(another_lecturer, Lecturer):
            return self.get_average_grade() < another_lecturer.get_average_grade()
        else:
            return 'Ошибка. Сравнивать можно только с другим лекторами'


class Reviewer(Mentor):

    def rate(self, student, course, grade):
        if (isinstance(student, Student) and course in self.courses_attached
                and course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f'Имя: {self.name}\n Фамилия: {self.surname}'


def get_avg_students_grade(students, course):
    if not students or not course:
        return 'Нет данных'
    avg_grades = []
    for student in students:
        student_grade = average(
            [grade for course, grade in student.grades.items() if course == course]
        ) or 0
        avg_grades.append(student_grade)
    return average(avg_grades)


def get_avg_lecturers_grade(lecturers, course):
    if not lecturers or not course:
        return 'Нет данных'
    avg_grades = []
    for lecturer in lecturers:
        lecturer_grade = average(
            [grade for course, grade in lecturer.grades.items() if course == course]
        ) or 0
        avg_grades.append(lecturer_grade)
    return average(avg_grades)


first_student = Student('Ruoy', 'Eman', 'male')
first_student.courses_in_progress += ['Python']

second_student = Student('John', 'Watters', 'male')
second_student.courses_in_progress += ['Python']

first_lector = Lecturer('Will', 'Smith')
first_lector.courses_attached += ['Python']

second_lector = Lecturer('Some', 'Buddy')
second_lector.courses_attached += ['Python']

first_reviewer = Reviewer('Nik', 'Bez')
first_reviewer.courses_attached += ['Python']

first_student.rate_lection(first_lector, 'Python', 10)
first_student.rate_lection(first_lector, 'Python', 5)

first_student.rate_lection(second_lector, 'Python', 1)
first_student.rate_lection(second_lector, 'Python', 2)


first_reviewer.rate(first_student, 'Python', 10)
first_reviewer.rate(first_student, 'Python', 1)
first_reviewer.rate(second_student, 'Python', 5)

avg_st_gr = get_avg_students_grade([first_student, second_student], 'Python')
avg_lt_gr = get_avg_lecturers_grade([first_lector, second_lector], 'Python')


print(first_lector)
print(first_student)
print(first_student > second_student)
print(first_lector < second_lector)
print('Средняя оценка студента: ', avg_st_gr)
print('Средняя оценка лектора: ', avg_lt_gr)
