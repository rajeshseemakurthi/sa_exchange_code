# index page
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from server import app
from flask_login import logout_user, current_user

# app pages
from pages import (
    c_clinics_conducted,
    c_mp,
    c_ncd_breakup,
    c_ncd,
    c_revisits,
    c_tbv,
    c_tests_conducted,
    c_unique_registrations,
    home,
    login,
    register
)

# app authentication 
from pages import (
    login,
    register,
)

header = dbc.Navbar(
    dbc.Container(
        [
            # dbc.NavbarBrand("Dash Auth Flow", href="/home"),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Home", href="/home"),className="Home"),
                    dbc.NavItem(dbc.NavLink("Refresh", href="/",id="refresh_initial")),
                    dbc.NavItem(dbc.NavLink(id='user-name',href='/profile')),
                    dbc.NavItem(dbc.NavLink('Login',id='user-action',href='Login'))
                ],className="navItems"
            )
        ]
    ),
    className="mb-5",
)



app.layout = html.Div(
    [
        header,
        html.Div(
            [
                dbc.Container(
                    id='page-content'
                )
            ]
        ),
        dcc.Location(id='base-url', refresh=True)
    ]
)


@app.callback(
    Output('refresh_initial','href'),
    Output('page-content', 'children'),
    [Input('base-url', 'pathname')])
def router(pathname):
    '''
    routes to correct page based on pathname
    '''
    # for debug
    print('routing to',pathname)
    
    # auth pages
    if pathname == '/login':
        if not current_user.is_authenticated:
            return login.layout(),'/login'
    elif pathname =='/register':
        if not current_user.is_authenticated:
            return register.layout(),'/register'
    # elif pathname == '/change':
    #     if not current_user.is_authenticated:
    #         return change_password.layout(),pathname
    # elif pathname == '/forgot':
    #     if not current_user.is_authenticated:
    #         return forgot_password.layout(),pathname
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user(),'/logout'
    
    # app pages
    elif pathname == '/' or pathname=='/home' or pathname=='/home':
        if current_user.is_authenticated:
            return home.layout(),'/home'
    # elif pathname == '/profile' or pathname=='/profile':
    #     if current_user.is_authenticated:
    #         return profile.layout(),'/profile'
    # elif pathname == '/page1' or pathname=='/page1':
    #     if current_user.is_authenticated:
    #         return page1.layout(),'/page1'
    #c_unique_registrations
    elif pathname == '/c_unique_registrations':
        if current_user.is_authenticated:
            return c_unique_registrations.layout(),'/c_unique_registrations'
        elif not current_user.is_authenticated:
            logout_user()
            return login.layout(),'/login'
    #c_tests_conducted
    elif pathname == '/c_tests_conducted':
        if current_user.is_authenticated:
            return c_tests_conducted.layout(),'/c_tests_conducted'
        elif not current_user.is_authenticated:
            logout_user()
            return login.layout(),'/login'
    #c_tbv
    elif pathname == '/c_tbv':
        if current_user.is_authenticated:
            return c_tbv.layout(),'/c_tbv'
        elif not current_user.is_authenticated:
            logout_user()
            return login.layout(),'/login'
    #c_revisits
    elif pathname == '/c_revisits':
        if current_user.is_authenticated:
            return c_revisits.layout(),'/c_revisits'
        elif not current_user.is_authenticated:
            logout_user()
            return login.layout(),'/login'
    #c_ncd
    elif pathname == '/c_ncd':
        if current_user.is_authenticated:
            return c_ncd.layout(),'/c_ncd'
        elif not current_user.is_authenticated:
            logout_user()
            return login.layout(),'/login'
    #c_ncd_breakup
    elif pathname == '/c_ncd_breakup':
        if current_user.is_authenticated:
            return c_ncd_breakup.layout(),'/c_ncd_breakup'
        elif not current_user.is_authenticated:
            logout_user()
            return login.layout(),'/login'
    #c_mp
    elif pathname == '/c_mp':
        if current_user.is_authenticated:
            return c_mp.layout(),'/c_mp'
        elif not current_user.is_authenticated:
            logout_user()
            return login.layout(),'/login'
    #c_clinics_conducted
    elif pathname == '/c_clinics_conducted':
        if current_user.is_authenticated:
            return c_clinics_conducted.layout(),'/c_clinics_conducted'
        elif not current_user.is_authenticated:
            logout_user()
            return login.layout(),'/login'


    # DEFAULT LOGGED IN: /home
    if current_user.is_authenticated:
        return home.layout(),'/home'
    
    # DEFAULT NOT LOGGED IN: /login
    return login.layout(),'/login'


@app.callback(
    Output('user-name', 'children'),
    [Input('page-content', 'children')])
def profile_link(content):
    '''
    returns a navbar link to the user profile if the user is authenticated
    '''
    if current_user.is_authenticated:
        return html.Div(current_user.first)
    else:
        return ''


@app.callback(
    [Output('user-action', 'children'),
     Output('user-action','href')],
    [Input('page-content', 'children')])
def user_logout(input1):
    '''
    returns a navbar link to /logout or /login, respectively, if the user is authenticated or not
    '''
    if current_user.is_authenticated:
        return 'Logout', '/logout'
    else:
        return 'Login', '/login'
    
# @app.callback(Output("refresh_initial","href"),Input("base-url","pathname"))
# def url_route(pathname):
    

if __name__ == '__main__':
    app.run_server(debug=True)
