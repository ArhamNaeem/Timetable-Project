from reactpy import component, html, run, use_state, use_effect
from timetable_generation import class_timetable as ct, teacher_timetable as tt
@component
def Class_Timetable():
     headers = list(ct[0].keys())
     th_elements = []
     tr_elements = []
     current_semester = None
     for header in headers:
        if header!= 'semester':
         th_elements.append(html.th(header))
     for i in range(len(ct)):
         tr_elements.append([])
         td_elements = []
         table_caption = []
         for key,value in ct[i].items():
          if(key != 'semester'):  
             if(current_semester != ct[i]['semester']):
               current_semester = ct[i]['semester']
               table_caption = html.caption(html.h1(f'Timetable for Semester {current_semester}'))
               tr_elements[i].append(html.tr(table_caption))
               tr_elements[i].append(html.tr(*th_elements))
             td_elements.append(html.td(value))
         tr_elements[i].append(html.tr(td_elements))
  
     return html.table(
            {"border":"1"},
            #  *table_captions
            #   html.tr(th_elements),
              *tr_elements
           )  
@component
def Teacher_Timetable():
     headers = list(tt[0].keys())
     th_elements = []
     tr_elements = []
     current_teacher = None
     for header in headers:
        if header!= 'teacherName':
         th_elements.append(html.th(header))
     for i in range(len(tt)):
         tr_elements.append([])
         td_elements = []
         table_caption = []
         for key,value in tt[i].items():
          if(key != 'teacherName'):  
             if(current_teacher != ct[i]['teacher']):
               current_teacher = ct[i]['teacher']
               table_caption = html.caption(html.h1(f'Timetable for {current_teacher}'))
               tr_elements[i].append(html.tr(table_caption))
               tr_elements[i].append(html.tr(*th_elements))
             td_elements.append(html.td(value))
         tr_elements[i].append(html.tr(td_elements))
  
     return html.table(
            {"border":"1"},
            #  *table_captions
            #   html.tr(th_elements),
              *tr_elements
           )


@component
def GetTimetable(query):
  if query:
   print(query)          
   return html.h1('hi')

@component
def ShowTimeTable(state):
  val, set_val = use_state("")
  query , set_query = use_state("")
  def handleClick(event):
    if event['currentTarget']['value'] == 'Student' and int(val) <=0 or int(val)>8:
      print('Invalid semester!')
      set_val("")
      return
    set_query({'position':event['currentTarget']['value'],'value':val})
   
  def handleChange(event):
    set_val(val + event['currentTarget']['value'])
  if state:
    input = None
    if state == 'Student':
     return html.div( html.input({'placeholder':"Enter your semester",'on_change':handleChange}),
      html.button({'on_click':handleClick,"value":"Student"},'Check timetable'),
        GetTimetable(query)
     )
     
    return html.div (html.input({'placeholder':"Enter your name",'on_change':handleChange}),
      html.button({'on_click':handleClick,"value":'Teacher'},'Check timetable'),
      GetTimetable(query)
      )
 
    
      
       

@component
def UserInteraction():
  state, set_state = use_state(None)
  def handleSubmit(event):
    set_state(event['currentTarget']['value'])
  htmlButtons=None
  if not state:
    htmlButtons = [html.button({"on_click":handleSubmit,'value':'Student'},'Are you a student'), 
   html.button({"on_click":handleSubmit, "value":'Teacher'},'Are you a teacher') ]
  if state: 
    htmlButtons = ""
  return html.div(
    *htmlButtons,
  ShowTimeTable(state) 
  
 
  )
  
@component
def App():
  return html.div(
    UserInteraction(),
    # Class_Timetable(),
    # Teacher_Timetable()
  )


run(App)