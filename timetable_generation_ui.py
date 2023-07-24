from reactpy import component, html, run, use_state, use_effect
from timetable_generation import class_timetable as ct, teacher_timetable as tt
from timetable_generation import teachers,max_lectures_per_day,teacherSubjectsTaught,rooms,days,time_slots, timetable_generator
from timetable_generation import TimetableGenerator
import pandas as pd
tt_generator = timetable_generator
class_tt = ct
teacher_tt = tt

# TODO 1: MAKE ROOMS BE SELECTED FROM 1-END NOT JUST 1
# TODO 2: ALLOW AUTO FIXTURE, IF TEACHER IS ABSENT ANOTHER TEACHER SHALL BE ALLOCATED


subjects=pd.read_csv("subjects.csv")
subjects = [subject.split(',') for subject in subjects['subject']]

        
@component
def Class_Timetable(semester):
     global class_tt
     semester = int(semester)
     headers = list(ct[0].keys())
     th_elements = []
     tr_elements = []
    #  current_semester = None
     for header in headers:
        if header!= 'semester':
         th_elements.append(html.th(header))
     for i in range(len(class_tt)):
         tr_elements.append([])
         td_elements = []
         table_caption = []
         if class_tt[i]['semester'] == semester:
          # print('here')
          for key,value in class_tt[i].items():
            if(key != 'semester'):  
                # tr_elements[i].append(html.tr(*th_elements))
                td_elements.append(html.td(value))
          tr_elements[i].append(html.tr(td_elements))
    #  print(tr_elements)
     return html.table(
            {"border":"1"},
             html.caption(html.h1(f'Timetable for semester {semester}')),
              html.tr(th_elements),
              *tr_elements
           )  
@component
def Teacher_Timetable(_teacher):
     global teacher_tt
     headers = list(tt[0].keys())
     th_elements = []
     tr_elements = []
     for header in headers:
        if header!= 'teacherName':
         th_elements.append(html.th(header))
     for i in range(len(teacher_tt)):
         tr_elements.append([])
         td_elements = []
         table_caption = []
         print(_teacher,teacher_tt[i]['teacherName'])
         if teacher_tt[i]['teacherName'] == _teacher:
          for key,value in teacher_tt[i].items():
            #  print(key)
             if(key != 'teacherName'):  
                #  tr_elements[i].append(html.tr(*th_elements))
                td_elements.append(html.td(value))
          tr_elements[i].append(html.tr(td_elements))
   
    
     return html.table(
            {"border":"1"},
            #  *table_captions
            html.caption(html.h1(f'Timetable for {_teacher}')),
              html.tr(th_elements),
              *tr_elements
           )

@component
def GenerateNewTimetable(state):
  if state:
    global class_tt
    global teacher_tt_tt
    global subjects
    global tt_generator
    new_subjects=pd.read_csv("subjects.csv")
    new_subjects = [subject.split(',') for subject in new_subjects['subject']]
    subjects=new_subjects
    # print(new_subjects)
    tt_generator = TimetableGenerator(subjects,teachers,max_lectures_per_day,teacherSubjectsTaught,rooms,days,time_slots)
    # print('new timetable generated')
    # print(class_tt)
    
    ct,tt= tt_generator.generate_timetable()
    class_tt = ct
    teacher_tt = tt
    # print(class_tt)
    
    
  
@component
def FileUploadComponent():
     state ,set_state= use_state(False)
     def handleClick(event):
       set_state(True)
     return html.div(
       html.h1('Requirements for uploading file'),
       html.ul(
         html.li('Upload csv file only'),
         html.li('File must be named subjects.csv'),
         html.li(
           "File must have",
           html.ul(
             html.li('2 columns'),
             html.li('Column 1 must be semester_id, specifying semester number'),
             html.li('Column 2 must be subject, specifying subjects to be taught in this semester')
           )
         )
       ),
        html.form(
            {'action': ' http://127.0.0.1:5000/upload-timetable', 'method': 'POST', 'enctype': 'multipart/form-data'},
            html.input({'type': 'file', 'name': 'file'}),
            html.button({'type': 'submit','on_click':handleClick}, 'Generate Timetable')
        ),
        GenerateNewTimetable(state)
    )  
     
     
     
@component
def AttendanceUploadComponent():
     state ,set_state= use_state(False)
     def handleClick(event):
       set_state(True)
     return html.div(
       html.h1('Requirements for uploading file'),
       html.ul(
         html.li('Upload csv file only'),
         html.li('File must be named attendance.csv'),
         html.li(
           "File must have",
           html.ul(
             html.li('3 columns'),
             html.li("Column 1 must be teacher_id, specifying teacher's unique id"),
             html.li("Column 2 must be teacher_name, specifying teacher's name"),
             html.li('Column 3 must be attendance_status, specifying their presence')
           )
         )
       ),
        html.form(
            {'action': ' http://127.0.0.1:5000/upload-attendance', 'method': 'POST', 'enctype': 'multipart/form-data'},
            html.input({'type': 'file', 'name': 'file'}),
            html.button({'type': 'submit','on_click':handleClick}, 'Add attendance')
        ),
        # GenerateNewTimetable(state)
    )  



@component
def GetTimetable(query):
  if query:
    # print(query['position'],query['value'])
    if query['position']=='Student':           
      return html.div(
        Class_Timetable(query['value'])
      )
    if query['position'] == 'Teacher':
      return html.div(
       
        Teacher_Timetable(query['value'])
      )
      
@component
def ShowAllocation(show_allocation,state,semester,course):
  if show_allocation:
    # print(show_allocation)
    return html.div(
      f"{state['room']} has been assigned to semester {semester} for {course} class on {state['day']} at time {state['timeslot']}"
    )
    
      
    
    
    
      
@component 
def AllocateRoom(available_rooms,timetable):
  name,set_name = use_state(None)
  semester,set_semester = use_state(None)
  course,set_course = use_state(None)
  day,set_day = use_state(None)
  state , set_state= use_state(None)
  show_allocation,set_show_allocation = use_state(False)
  def changeName(event):
    set_name(event['currentTarget']['value'])
  def changeSemester(event):
    set_semester(event['currentTarget']['value'])
  def changeCourse(event):
    set_course(event['currentTarget']['value'])
  def changeDay(event):
    set_day(event['currentTarget']['value'])
    
    
  def handleSubmit(event):
    global teacher_tt
    ret= timetable.allocate_room(day,name,semester,course,teacher_tt)
    # print(ret)
    if ret:
     set_state(ret)
     set_show_allocation(True)
    if  not ret:
      set_show_allocation(False)
    
  return html.div(
    html.input({'placeholder':'Enter teacher name','on_change':changeName}),
    html.input({'placeholder':'Enter semester','on_change':changeSemester}),
    html.input({'placeholder':'Enter course name','on_change':changeCourse}),
    html.input({'placeholder':'Enter day of extra class','on_change':changeDay}),
    html.button({'on_click':handleSubmit},'Allocate Room'),
    ShowAllocation(show_allocation,state,semester,course)
  )  
  
  
      
@component
def ExtraClassComponent():
    global tt_generator
    global subjects
    tr_elements = []
    new_subjects=pd.read_csv("subjects.csv")
    new_subjects = [subject.split(',') for subject in new_subjects['subject']]
    subjects=new_subjects
    available_rooms = tt_generator.show_available_rooms_timeslots()
    tr_elements=[]
    for available_room in available_rooms:
        tr_elements.append(html.tr(html.td(available_room['day']),html.td(available_room['room']),html.td(available_room['timeslot'])))
    return html.div(
      AllocateRoom(available_rooms,tt_generator),
      html.h1('Available rooms'),
    html.table(
      {"border":"1"},
     html.tr([html.th('Day'), html.th('Room'), html.th('Timeslot')]),
     *tr_elements
  
  )
    )
  
  
  

@component
def ShowTimeTable(state):
  val, set_val = use_state("")
  query , set_query = use_state("")
  
  # def handleFile(event):
    # print(event)
  
  def handleClick(event):
    print(event['currentTarget']['value'],val)
    if event['currentTarget']['value'] == 'Teacher':
     set_query({'position':event['currentTarget']['value'],'value':val})
     return 
      
    if event['currentTarget']['value'] == 'Student' and int(val) <=0 or int(val)>8:
      print('Invalid semester!')
      set_val("")
      return
    else:
     set_query({'position':event['currentTarget']['value'],'value':val})
     return 
   
  def handleChange(event):
    set_val(event['currentTarget']['value'])
  if state:
    input = None
    if state == 'Student':
     return html.div( html.input({'placeholder':"Enter your semester",'on_change':handleChange}),
      html.button({'on_click':handleClick,"value":"Student"},'Check timetable'),
        GetTimetable(query)
     )
    if state == 'Teacher':
     
      return html.div (html.input({'placeholder':"Enter your name",'on_change':handleChange}),
      html.button({'on_click':handleClick,"value":'Teacher'},'Check timetable'),
      GetTimetable(query)
      )
    if state == 'GenerateTT':
      return html.div(
      FileUploadComponent() 
      )
    if state == 'AddAttendance':
        return html.div(
          AttendanceUploadComponent()
        )
    if state == 'AddExtraClass':
      return html.div(
        ExtraClassComponent()
        
        )
    if state == 'AssignSubstitute':
      return html.div(
        AssignSubstituteComponent()
      )
      
 
@component
def AssignSubstituteComponent():
  global tt_generator
  global teacher_tt
  list = tt_generator.substitution(teacher_tt)
  tr_elements = []
  # print(list)
  if not list:
    return html.div(
      'Could not add fixture'
    )
  for items in list:
    tr_elements.append(html.tr(f'{items[0]} is teaching {items[1]} in place of {items[2]}'))
  return html.table(
    html.caption(
    'Successfully added a fixture for absent teachers'
    ),
    *tr_elements
  )

@component
def UserInteraction():
  state, set_state = use_state(None)
  def handleSubmit(event):
    set_state(event['currentTarget']['value'])
  htmlButtons=None
  if not state:
    htmlButtons = [html.button({"on_click":handleSubmit,'value':'Student'},'Are you a student'), 
   html.button({"on_click":handleSubmit, "value":'Teacher'},'Are you a teacher') ,
   html.button({"on_click":handleSubmit, "value":'GenerateTT'},'Generate new timetable') ,
   html.button({"on_click":handleSubmit, "value":'AddAttendance'},"Add teacher's attendance record") ,
   html.button({"on_click":handleSubmit, "value":'AddExtraClass'},"Add extra class") ,
   html.button({"on_click":handleSubmit, "value":'AssignSubstitute'},"Assign Substitute") 
   
   
   ]
  if state: 
    htmlButtons = ""
  return html.div(
    *htmlButtons,
  ShowTimeTable(state) ,
  )
  
  
@component
def App():
  return html.div(
    UserInteraction()
  )


run(App)