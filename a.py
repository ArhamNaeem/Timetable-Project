import random

class TimetableGenerator:
    random.seed(43)
    def __init__(self, subjects, teachers, max_lectures_per_day, priority_subjects, topics, rooms, days, time_slots):
        self.subjects = subjects
        self.teachers = teachers
        self.max_lectures_per_day = max_lectures_per_day
        self.priority_subjects = priority_subjects
        self.topics = topics
        self.rooms = rooms
        self.days = days
        self.time_slots = time_slots
        self.teacher_timetable = {}
        self.student_timetable = {}

    def generate_timetable(self):
        self._initialize_timetables()

        for subject in self.subjects:
            self._assign_subject(subject)

        self._assign_remaining_slots()

    def _initialize_timetables(self):
        for teacher in self.teachers:
            self.teacher_timetable[teacher] = []
        
        for room in self.rooms:
            self.student_timetable[room] = {}
            
            for day in self.days:
                self.student_timetable[room][day] = {}
                
                for time_slot in self.time_slots:
                    self.student_timetable[room][day][time_slot] = []

    def _assign_subject(self, subject):
        topic = self._select_topic(subject)
        teacher = self._select_teacher(subject)
        room = self._select_room(teacher)

        if topic and teacher and room:
            day, time_slot = self._select_time_slot(room, teacher)

            if day and time_slot:
                self.teacher_timetable[teacher].append((subject, room, day, time_slot))
                self.student_timetable[room][day][time_slot].append((subject, teacher))

    def _assign_remaining_slots(self):
        for teacher in self.teachers:
            while len(self.teacher_timetable[teacher]) < self.max_lectures_per_day:
                subject = random.choice(self.subjects)
                room = self._select_room(teacher)
                day, time_slot = self._select_time_slot(room, teacher)

                if subject and room and day and time_slot:
                    self.teacher_timetable[teacher].append((subject, room, day, time_slot))
                    self.student_timetable[room][day][time_slot].append((subject, teacher))

    def _select_topic(self, subject):
        if subject in self.priority_subjects:
            return random.choice(self.topics[subject])

        for topic in self.topics[subject]:
            for day in self.days:
                for time_slot in self.time_slots:
                    if not self._is_topic_scheduled(subject, topic, day, time_slot):
                        return topic

        return None

    def _is_topic_scheduled(self, subject, topic, day, time_slot):
        for teacher, timetable in self.teacher_timetable.items():
            for entry in timetable:
                if entry[0] == subject and entry[2] == day and entry[3] == time_slot:
                    return True

        return False

    def _select_teacher(self, subject):
        available_teachers = [teacher for teacher in self.teachers if self._can_teach(teacher, subject)]

        if available_teachers:
            return random.choice(available_teachers)

        return None

    def _can_teach(self, teacher, subject):
        return len(self.teacher_timetable[teacher]) < self.max_lectures_per_day

    def _select_room(self, teacher):
        occupied_rooms = set(entry[1] for entry in self.teacher_timetable[teacher])
        available_rooms = [room for room in self.rooms if room not in occupied_rooms]

        if available_rooms:
            return random.choice(available_rooms)

        return None

    def _select_time_slot(self, room, teacher):
        for day in self.days:
            for time_slot in self.time_slots:
                if not self._is_occupied(room, day, time_slot):
                    return day, time_slot

        return None, None

    def _is_occupied(self, room, day, time_slot):
        return bool(self.student_timetable[room][day][time_slot])

    def mark_teacher_absent(self, teacher, room, day, time_slot):
        for entry in self.teacher_timetable[teacher]:
            if entry[1] == room and entry[2] == day and entry[3] == time_slot:
                self.teacher_timetable[teacher].remove(entry)
                self._assign_alternate_teacher(entry[0], entry[2], entry[3])
                break

    def _assign_alternate_teacher(self, subject, day, time_slot):
        available_teachers = [teacher for teacher in self.teachers if self._can_teach(teacher, subject)]

        if available_teachers:
            new_teacher = random.choice(available_teachers)
            room = self._select_room(new_teacher)
            self.teacher_timetable[new_teacher].append((subject, room, day, time_slot))
            self.student_timetable[room][day][time_slot].append((subject, new_teacher))

    def mark_teacher_present(self, teacher, day, time_slot):
        for entry in self.teacher_timetable[teacher]:
            if entry[2] == day and entry[3] == time_slot:
                return  # Teacher is already marked present for the given slot

        subject = self.student_timetable[room][day][time_slot][0][0]
        room = self.student_timetable[room][day][time_slot][0][1]
        self.teacher_timetable[teacher].append((subject, room, day, time_slot))

    def print_timetables(self):
        print("Teacher Timetable:")
        for teacher, timetable in self.teacher_timetable.items():
            print("Teacher:", teacher)
            for entry in timetable:
                print("Subject:", entry[0], "| Room:", entry[1], "| Day:", entry[2], "| Time Slot:", entry[3])
            print()

        print("\nStudent Timetable:")
        for room, timetable in self.student_timetable.items():
            print("Room:", room)
            for day, slots in timetable.items():
                for time_slot, entries in slots.items():
                    for entry in entries:
                        subject = entry[0]
                        teacher = entry[1]
                        print("Subject:", subject, "| Room:", room, "| Day:", day, "| Time Slot:", time_slot, "| Teacher:", teacher)
            print()

    def has_min_subjects_per_day(self):
        for room, timetable in self.student_timetable.items():
            for day, slots in timetable.items():
                subjects = set()
                for time_slot, entries in slots.items():
                    for entry in entries:
                        subject = entry[0]
                        subjects.add(subject)
                if len(subjects) < 2:
                    return False
        return True


# Example usage
subjects = ["Math", "English", "Science", "History", "Geography", "Physics", "Chemistry", "Biology", "Computer Science", "Physical Education"]
teachers = ["Mr. Smith", "Ms. Johnson", "Mr. Brown", "Ms. Davis", "Mr. Wilson", "Mrs. Anderson", "Mr. Thompson", "Ms. Roberts", "Mr. Clark", "Mrs. Moore"]
max_lectures_per_day = 3
priority_subjects = ["Math", "Science", "English"]
topics = {
    "Math": ["Algebra", "Geometry", "Calculus", "Statistics"],
    "English": ["Grammar", "Literature", "Writing"],
    "Science": ["Physics", "Chemistry", "Biology", "Environmental Science"],
    "History": ["World History", "American History", "European History"],
    "Geography": ["Physical Geography", "Human Geography", "Geopolitics"],
    "Physics": ["Mechanics", "Thermodynamics", "Optics"],
    "Chemistry": ["Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry"],
    "Biology": ["Cell Biology", "Genetics", "Ecology"],
    "Computer Science": ["Programming", "Data Structures", "Algorithms"],
    "Physical Education": ["Sports", "Fitness", "Health Education"]
}
rooms = ["Room 1", "Room 2", "Room 3", "Room 4", "Room 5", "Room 6", "Room 7", "Room 8", "Room 9", "Room 10"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
time_slots = ["9:00 AM - 10:00 AM", "10:00 AM - 11:00 AM", "11:00 AM - 12:00 PM", "1:00 PM - 2:00 PM", "2:00 PM - 3:00 PM"]

timetable_generator = TimetableGenerator(subjects, teachers, max_lectures_per_day, priority_subjects, topics, rooms, days, time_slots)
timetable_generator.generate_timetable()

# while not timetable_generator.has_min_subjects_per_day():
#     timetable_generator.generate_timetable()
#     timetable_generator.print_timetables()


# Marking a teacher absent for a specific day and time slot
absent_teacher = "Mr. Smith"
absent_room = "Room 2"
absent_day = "Monday"
absent_time_slot = "9:00 AM - 10:00 AM"
timetable_generator.mark_teacher_absent(absent_teacher, absent_room, absent_day, absent_time_slot)

# Printing the timetables
timetable_generator.print_timetables()
