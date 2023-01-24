import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
from dash import no_update

from flask_login import login_user, current_user
from werkzeug.security import check_password_hash
import time
from validate_email import validate_email

from server import app,User_1,session,engine
# from utilities.auth import (
#     add_user,
#     user_exists,
#     db,
# )

def user_exists(email:str,engine)->bool:
    user=session.query(User_1).filter(User_1.email==email).first()
    if user:
        return True
    else:
        return False
    
def add_user(username,email,password,engine)->bool:
    p1=User_1(username,email,password)
    try:
        session.add(p1)
        session.commit()
        return True
    except:
        return False

success_alert = dbc.Alert(
    'Registered successfully. Taking you to login.',
    color='success',
    dismissable=True
)
failure_alert = dbc.Alert(
    'Registration unsuccessful.',
    color='danger',
    dismissable=True
)
already_registered_alert = dbc.Alert(
    "You're already registered! Taking you home.",
    color='success',
    dismissable=True
)

def layout():
    return dbc.Row(
        dbc.Col(
            [
                dcc.Location(id='register-url',refresh=True,),
                html.Div(id='register-trigger',style=dict(display='none')),
                html.Div(id='register-alert'),
                dbc.FormGroup(
                    [
                        dbc.FormText('UserName'),
                        dbc.Input(id='register-username',autoFocus=True),
                        html.Br(),

                        dbc.FormText('Email',id='register-email-formtext',color='secondary'),                        
                        dbc.Input(id='register-email'),
                        html.Br(),

                        dbc.FormText('Password'),                        
                        dbc.Input(id='register-password',type='password'),
                        html.Br(),

                        dbc.FormText('Confirm password'),                        
                        dbc.Input(id='register-confirm',type='password'),
                        html.Br(),
                        

                        dbc.Button('Submit',color='primary',id='register-button'),
                    ]
                )
            ],
            width=6
        )
    )




@app.callback(
    [Output('register-'+x,'valid') for x in ['username','email','password','confirm']]+\
    [Output('register-'+x,'invalid') for x in ['username','email','password','confirm']]+\
    [Output('register-button','disabled'),
     Output('register-email-formtext','children'),
     Output('register-email-formtext','color')],
    [Input('register-'+x,'value') for x in ['username','email','password','confirm']]
)
def register_validate_inputs(username,email,password,confirm):
    '''
    validate all inputs
    '''
    
    email_formtext = 'Email'
    email_formcolor = 'secondary'
    disabled = True
    bad = [None,'']
    
    v = {k:f for k,f in zip(['username','email','password','confirm'],[username,email,password,confirm])}
    # if all the values are empty, leave everything blank and disable button
    if sum([x in bad for x in v.values()])==4:
        return [False for x in range(8)]+[disabled,email_formtext,email_formcolor]

    d = {}
    d['valid'] = {x:False for x in ['username','email','password','confirm']}
    d['invalid'] = {x:False for x in ['username','email','password','confirm']}

    def validate(x, inst):
        if v[x] in bad:
            pass
        elif not isinstance(v[x],inst):
            d['valid'][x], d['invalid'][x] = False,True
        else:
            d['valid'][x], d['invalid'][x] = True, False

    #Default in Code
    for k in ['username','password']:
        validate(k,str)

    #Which Manually created
    for m in ['email','password']:
        validate(m,str)

    x = 'confirm'
    if v[x] in bad:
        pass
    d['valid'][x] = not v[x]in bad and v['password']==v[x]
    d['invalid'][x] = not v['confirm']


    # if it's a valid email, check if it already exists
    # if it exists, invalidate it and let the user know
    x = 'email'
    if v[x] in bad:
        pass
    else: 
        d['valid'][x] = validate_email(v[x])
        d['invalid'][x] = not d['valid'][x]
    if user_exists(v[x],engine):
        d['valid'][x] = False
        d['invalid'][x] = True
        email_formcolor = 'danger'
        email_formtext = 'Email already exists.'
    
    # if all are valid, enable the button
    if sum(d['valid'].values())==5:
        disabled = False

    return [
        *list(d['valid'].values()),
        *list(d['invalid'].values()),
        disabled,
        email_formtext,
        email_formcolor
    ]


@app.callback(
    [Output('register-url', 'pathname'),
     Output('register-alert', 'children')],
    [Input('register-button', 'n_clicks')],
    [State('register-'+x, 'value') for x in ['username','email','password','confirm']],
)
def register_success(n_clicks,username,email,password,confirm):
    if n_clicks == 0:
        time.sleep(.25)
        if current_user.is_authenticated:
            return '/home',already_registered_alert
        else:
            return no_update,no_update
    
    if add_user(username,password,email,engine):
        return '/login',success_alert
    else:
        return '',failure_alert