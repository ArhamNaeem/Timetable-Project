from reactpy import component, html, run,hooks


# @component
# def App():
#      count ,set_count = hooks.use_state(0)
#      def handleClick(event):
#          set_count(count+1)
#      return html.div(
#          html.p(count),
#          html.button({"on_click":handleClick},"ClickME")
         
#      )
@component
def App():
    return html.table(
        {"border":"1"},
        
     html.tr(
         html.th('c1'),
         html.th('c2'),
         html.th('c3'),
         html.th('c4')
     )  , 
     html.tr(
         html.td('1'),
         html.td('2'),
         html.td('3'),
         html.td('4')
     ) 
    )

run(App)