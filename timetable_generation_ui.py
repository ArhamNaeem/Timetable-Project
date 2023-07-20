from reactpy import component, html, run, use_state, use_effect
from timetable_generation import class_timetable as ct, teacher_timetable as tt
from timetable_generation import teachers,max_lectures_per_day,teacherSubjectsTaught,rooms,days,time_slots
from timetable_generation import TimetableGenerator
import pandas as pd

class_tt = ct
teacher_tt = tt

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
    new_subjects=pd.read_csv("subjects.csv")
    new_subjects = [subject.split(',') for subject in new_subjects['subject']]
    subjects=new_subjects
    # print(new_subjects)
    timetable = TimetableGenerator(subjects,teachers,max_lectures_per_day,teacherSubjectsTaught,rooms,days,time_slots)
    print('new timetable generated')
    print(class_tt)
    
    ct,tt= timetable.generate_timetable()
    class_tt = ct
    teacher_tt = tt
    print(class_tt)
    
    
  
@component
def FileUploadComponent():
     state ,set_state= use_state(False)
     def handleClick(event):
      #  print('here')
       set_state(True)
     return html.div(
       html.h1('Requirements for uploading file'),
       html.ul(
         html.li('Upload csv file only'),
         html.li('File must be named students.csv'),
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
            {'action': ' http://127.0.0.1:5000/upload', 'method': 'POST', 'enctype': 'multipart/form-data'},
            html.input({'type': 'file', 'name': 'file'}),
            html.button({'type': 'submit','on_click':handleClick}, 'Generate Timetable')
        ),
        GenerateNewTimetable(state)
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
def ShowTimeTable(state):
  val, set_val = use_state("")
  query , set_query = use_state("")
  
  def handleFile(event):
    print(event)
  
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
      set_upload_file(True)
 
    
      
     

@component
def UserInteraction():
  state, set_state = use_state(None)
  def handleSubmit(event):
    set_state(event['currentTarget']['value'])
  htmlButtons=None
  if not state:
    htmlButtons = [html.button({"on_click":handleSubmit,'value':'Student'},'Are you a student'), 
   html.button({"on_click":handleSubmit, "value":'Teacher'},'Are you a teacher') ,
   html.button({"on_click":handleSubmit, "value":'GenerateTT'},'Generate new timetable') 
   
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
    UserInteraction(),
    # Class_Timetable(),
    # Teacher_Timetable()
  )


run(App)