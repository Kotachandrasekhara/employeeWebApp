from student import Student

students = []

class HighSchoolStudent(Student):

    school_name = "Citros Garden High school"

    def get_name_capitalize(self):
        original_value = super().get_name_capitalize()
        return original_value + "-HS"

    def get_school_name(self):
        return "This is HS Student"

