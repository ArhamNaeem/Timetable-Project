import random

from tabulate import tabulate

import pandas as pd

subjects=pd.read_csv("subjects.csv")

subjects = [subject.split(',') for subject in subjects['subject']]

        

# print(subjects)
class TimetableGenerator:

    def __init__(self, subjects, teachers, max_lectures_per_day,teacherSubjectsTaught , rooms, days, time_slots):
        random.seed(1)
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

            #get relevant teachers teaching the course
#              print(subject)
             available_teachers = [teacher for teacher,subjects_teaching in teacherSubjectsTaught.items() if subject in subjects_teaching]
#              print('subject',subject, available_teachers)
             self.selected_teachers.append({"teacher": available_teachers[random.randint(0,len(available_teachers)-1)],"subject":subject,"semester":_semester })
#              self.selected_teachers.append({"teacher": available_teachers[0],"subject":subject,"semester":_semester })

            _semester+=1

        for selected_teacher in self.selected_teachers:

         teacher = selected_teacher['teacher']

         subject = selected_teacher['subject']

         semester = selected_teacher['semester']

         for day in self.days:

            subject_taught = []

            tries = 10000

            while(tries):

                random_room = self.rooms[random.randint(0,len(self.rooms)-1)]

                random_time_slot = self.time_slots[random.randint(0,len(self.time_slots)-1)]

                while(subject not in subject_taught and  self.is_room_full[random_room][day][random_time_slot] == False and self.is_teacher_available[teacher][random_room][day][random_time_slot] and self.is_class_available[semester][day][random_time_slot]):

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

                            "semester":semester,
                            
                            "extra class": False
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

        return ct,tt
    # -------------------- ROOMS ARE NOT BEING ALLOCATED AFTER ROOM 1---------
    def allocate_room(self,day,teacher,semester,subject,teacher_tt):
        semester = int(semester)
        for room in self.rooms:
            for timeslot in self.time_slots:
                # print(self.is_room_full[room][day][timeslot])
                # print(self.is_class_available[semester][day][timeslot], timeslot,semester)
                if(self.is_room_full[room][day][timeslot]==False and self.is_teacher_available[teacher][room][day][timeslot] and self.is_class_available[semester][day][timeslot]):
                    details = {}
                    self.is_room_full[room][day][timeslot] = True
                    self.is_teacher_available[teacher][room][day][timeslot] = False
                    self.is_class_available[semester][day][timeslot]=False
                    teacher_tt.append({

                            "teacherName":teacher,

                            "subject":subject,

                            "day":day,

                            "room":room,

                            "time_slot":timeslot,

                            "semester":semester,
                            
                            "extra class": True
                        })
                    details['room']=room
                    details['day']=day
                    details['timeslot']=timeslot
                    return details
        return None
    def show_available_rooms_timeslots(self):
        free_room=[]
        for day in self.days:
            for room in self.rooms:
                for timeslot in self.time_slots:
                    # print(room,timeslot,day,self.is_room_full[room][day][timeslot],end="")
                    if(self.is_room_full[room][day][timeslot]==False):
                        # print('added',end="")
                        _temp = {}
                        _temp['room']=room
                        _temp['day']=day
                        _temp['timeslot']=timeslot
                        free_room.append(_temp)
                    # print()
        return free_room        
                        
    def print_semesterwise_timetable(self,timetable):

        print("--------Semester-Wise Timetable-------")

        timetable.sort(key=lambda x: x['semester'])

       

        semester_data = {}

        previous_semeter = None

        for row in timetable :

            semester = row['semester']

            if semester!= previous_semeter:

                previous_semeter = semester

                semester_data[semester] = []

            semester_data[semester].append(row)

        headers = [key for key in timetable[0].keys()  if key !='semester']  # Assuming all dictionaries have the same keys

        # # Convert the dictionaries to lists of values to create the table

        for semester, data in semester_data.items():

                print(f'Timetable for semester {semester}')

                       

                table_data = [[row[key] for key in headers] for row in data]

           

        # # Use the tabulate function to format and print the table

                print(tabulate(table_data, headers=headers, tablefmt="grid"))

   

    def print_teacher_timetable(self,timetable):

        print("-------Teacher's Timetable-----------")

        previous_teacher = None

        teacher_data = {}

        for row in timetable:

            teacher = row['teacherName']

            subject = row['subject']

            day = row['day']

            semester = row['semester']

            if previous_teacher != teacher:

                teacher_data[teacher] = []

                previous_teacher = teacher

            teacher_data[teacher].append(row)

        # print(teacher_data)

        headers = [key for key in timetable[0].keys() if key!='teacherName']

        for teacher, data in teacher_data.items():

            print(f'Timetable for teacher {teacher}')

            table_data = [[row[key] for key in headers] for row in data]

            print(tabulate(table_data, headers=headers, tablefmt="grid"))

           

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

    'Mr. Smith' : ['OOP','DCN'],

    'Ms. Johnson': ['Programming Fundamentals','ICT'],

    'Mr. Brown': ['English','Chemistry'],

    'Ms. Davis':['History','COAL'],

    'Mr. Wilson':['OOP','Programming Fundamentals'],

    'Mrs. Anderson': ['ICT','Computer Networks'],

    'Mr. Thompson': ['OOP','Math'],

    'Ms. Roberts': ['Programming Fundamentals','English'],

    'Mr. Clark': ['Chemistry','History'],

    'Mrs. Moore':['Science', 'DCN']

}

rooms = ["Room 1", "Room 2", "Room 3", "Room 4", "Room 5", "Room 6", "Room 7", "Room 8", "Room 9", "Room 10"]

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

time_slots = ["9:00 AM - 10:00 AM", "10:00 AM - 11:00 AM", "11:00 AM - 12:00 PM", "1:00 PM - 2:00 PM", "2:00 PM - 3:00 PM"]

timetable_generator = TimetableGenerator(subjects, teachers, max_lectures_per_day, teacherSubjectsTaught, rooms, days, time_slots)

class_timetable, teacher_timetable = timetable_generator.generate_timetable()

# ti/metable_generator.print_semesterwise_timetable(class_timetable)
# 
# timetable_generator.print_teacher_timetable(teacher_timetable) 
