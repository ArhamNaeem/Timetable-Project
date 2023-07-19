
import random
from tabulate import tabulate


class TimetableGenerator:
    def __init__(self, subjects, teachers, max_lectures_per_day,teacherSubjectsTaught , rooms, days, time_slots):
        self.subjects = subjects
        self.teachers = teachers
        self.max_lectures_per_day = max_lectures_per_day
        self.teacherSubjectsTaught= teacherSubjectsTaught
        self.rooms = rooms
        self.days = days
        self.time_slots = time_slots
        self.semester_number = 1
        
        self.teacher_timetable = {}
        self.student_timetable = {}
        self.is_room_full = {}
        self.is_teacher_available = {}
        self.selected_teachers = []
        self.is_class_available = {}
    def generate_timetable(self):
        self._initialize_timetables()
        tt = []
        ct = []
        #selecting teachers
        _semester = 1
        for subject_list in self.subjects:
            for subject in subject_list:
            #  print(subject)
            #get relevant teachers teaching the course
             available_teachers = [teacher for teacher,subjects_teaching in teacherSubjectsTaught.items() if subject in subjects_teaching]
            #  print(f'teachers available for {subject} are {available_teachers}')
             self.selected_teachers.append({"teacher": available_teachers[random.randint(0,len(available_teachers)-1)],"subject":subject,"semester":_semester })
            _semester+=1
        for selected_teacher in self.selected_teachers:
         teacher = selected_teacher['teacher']
         subject = selected_teacher['subject']
         semester = selected_teacher['semester']
         print(teacher,subject,"Sem",semester)
         for day in self.days:
            subject_taught = []
            tries = 10000
            while(tries):
                random_room = self.rooms[random.randint(0,len(self.rooms)-1)]
                random_time_slot = self.time_slots[random.randint(0,len(self.time_slots)-1)]
                while(subject not in subject_taught and not self.is_room_full[random_room][day][random_time_slot] and self.is_teacher_available[teacher][random_room][day][random_time_slot] and self.is_class_available[semester][day][random_time_slot]):
                        self.is_room_full[random_room][day][random_time_slot] = True
                        self.is_teacher_available[teacher][random_room][day][random_time_slot] = False
                        self.teacher_timetable[teacher][day][random_room][random_time_slot]= subject
                        self.is_class_available[semester][day][random_time_slot]=False
                        self.student_timetable[random_room][day][random_time_slot] =({teacher,subject})
                        subject_taught.append(subject)
                        tt.append({
                            "teacherName":teacher,
                            "subject":subject,
                            "day":day,
                            "room":random_room,
                            "time_slot":random_time_slot,
                            "semester":semester
                        })
                        ct.append({
                            "teacher":teacher,
                            "semester":semester,
                             "subject":subject,
                            "day":day,
                            "room":random_room,
                            "time_slot":random_time_slot
                        })
                       
                tries-=1
        print('Class timetable')
        for _ in ct:
            print(_)
        print('--------------------------------')
        print('Teacher timetable')
        
        for _ in tt:
            print(_)


        
    def _initialize_timetables(self):
    #every room is initially empty 
        for room in self.rooms:
            self.is_room_full[room]={}
            for day in self.days:
                self.is_room_full[room][day] = {}
                for time_slot in self.time_slots:
                 self.is_room_full[room][day][time_slot] = False
        for teacher in self.teachers:
         self.is_teacher_available[teacher]  = {}  
         for room in self.rooms:
            self.is_teacher_available[teacher][room] = {}
            for day in self.days:
                self.is_teacher_available[teacher][room][day]= {}
                for time_slot in self.time_slots:
                    self.is_teacher_available[teacher][room][day][time_slot]=True
     #every class is initially free
            
        for semester in range(1,8):
            self.is_class_available[semester] = {}
            for day in self.days:
                self.is_class_available[semester][day] = {}
                for time_slot in self.time_slots:
                    self.is_class_available[semester][day][time_slot] = True 
    #initalize timetable for teacher           
        for teacher in self.teachers:
            self.teacher_timetable[teacher] = {}
            for day in self.days:
              self.teacher_timetable[teacher][day] = {}
              for room in self.rooms:
                 self.teacher_timetable[teacher][day][room] = {}
                 for time_slot in self.time_slots:
                    self.teacher_timetable[teacher][day][room][time_slot]   = []
                    
    #initalize timetable for teacher           
    #can add semesters 1-8 or classes 1-10
    
        for room in self.rooms:
            self.student_timetable[room] = {}
            
            for day in self.days:
                self.student_timetable[room][day] = {}
                
                for time_slot in self.time_slots:
                    self.student_timetable[room][day][time_slot]   = None
                    
                    
                    
                    

# Example usage
semester_subjects = [["OOP","Programming Fundamentals","English","ICT","History","Computer Networks","COAL"],["Chemistry","Physics"]]


teachers = ["Mr. Smith", "Ms. Johnson", "Mr. Brown", "Ms. Davis", "Mr. Wilson", "Mrs. Anderson", "Mr. Thompson", "Ms. Roberts", "Mr. Clark", "Mrs. Moore"]
max_lectures_per_day = 4

teacherSubjectsTaught = {
    'Mr. Smith' : ['COAL','OOP'],
    'Ms. Johnson': ['ICT','English'],
    'Mr. Brown': ['Physics', 'Chemistry'],
    'Ms. Davis':['Histroy','English'],
    'Mr. Wilson':['OOP','Programming Fundamentals'],
    'Mrs. Anderson': ['ICT','Computer Networks'],
    'Mr. Thompson': ['OOP','Math'],
    'Ms. Roberts': ['Programming Fundamentals','English'],
    'Mr. Clark': ['Chemistry','History'],
    'Mrs. Moore':['Science, English']
}

rooms = ["Room 1", "Room 2", "Room 3", "Room 4", "Room 5", "Room 6", "Room 7", "Room 8", "Room 9", "Room 10"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
time_slots = ["9:00 AM - 10:00 AM", "10:00 AM - 11:00 AM", "11:00 AM - 12:00 PM", "1:00 PM - 2:00 PM", "2:00 PM - 3:00 PM"]
timetable_generator = TimetableGenerator(semester_subjects, teachers, max_lectures_per_day, teacherSubjectsTaught, rooms, days, time_slots)
timetable_generator.generate_timetable()

