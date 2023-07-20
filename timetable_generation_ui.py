from reactpy import component, html, run, use_state, use_effect
from timetable_generation import class_timetable as ct, teacher_timetable as tt
@component
def Class_Timetable(semester):
     semester = int(semester)
     headers = list(ct[0].keys())
     th_elements = []
     tr_elements = []
    #  current_semester = None
     for header in headers:
        if header!= 'semester':
         th_elements.append(html.th(header))
     for i in range(len(ct)):
         tr_elements.append([])
         td_elements = []
         table_caption = []
        #  print(ct[i]['semester'],semester,type(ct[i]['semester']),type(semester))
         if ct[i]['semester'] == semester:
          # print('here')
          for key,value in ct[i].items():
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
     headers = list(tt[0].keys())
     th_elements = []
     tr_elements = []
     for header in headers:
        if header!= 'teacherName':
         th_elements.append(html.th(header))
     for i in range(len(tt)):
         tr_elements.append([])
         td_elements = []
         table_caption = []
        #  print(_teacher,tt[i]['teacherName'])
         if tt[i]['teacherName'] == _teacher:
          for key,value in tt[i].items():
            #  print(key)
             if(key != 'teacherName'):  
                #  tr_elements[i].append(html.tr(*th_elements))
                td_elements.append(html.td(value))
          tr_elements[i].append(html.tr(td_elements))
     print(tr_elements)
    #  if(len(td_elements) ==0):
    #    return html.h1(
    #    'You have not been given any course to teach'
    #  )
     return html.table(
            {"border":"1"},
            #  *table_captions
            html.caption(html.h1(f'Timetable for {_teacher}')),
              html.tr(th_elements),
              *tr_elements
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