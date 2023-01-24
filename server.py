from sqlalchemy import create_engine,ForeignKey,Column,Integer,String,CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dash_bootstrap_components as dbc
from flask_login import LoginManager,UserMixin,logout_user,login_user,current_user
from dash import Dash,html,dcc,Input,Output
from flask_sqlalchemy import SQLAlchemy

Base=declarative_base()
db=SQLAlchemy()

class User_1(Base,UserMixin):
    __tablename__="USER_MAIN"
    
    id=Column("id",Integer,primary_key=True)
    username=Column("username",String(150),nullable=True)
    email=Column("email",String(150),unique=True)
    password=Column("password",String(200))
    
    def __init__(self,username,email,password):
        self.username=username
        self.email=email
        self.password=password
        
    def __repr__(self):
        return f"<User {self.id}>"

#Creating Connection with DB    
engine=create_engine("sqlite:///users_main.db",connect_args={'check_same_thread':False})
#combines our python class to DB
Base.metadata.create_all(bind=engine)

#Session class
Session=sessionmaker(autocommit=False,autoflush=False,bind=engine)
#Cretaing Instance of that Session
session=Session()

external_scripts = [
    {
        'src': 'https://code.jquery.com/jquery-3.6.1.js',
        'integrity': 'sha256-3zlB5s2uwoUzrXK3BT7AX3FyvojsraNFxCc2vC/7pNI=',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.9.2/umd/popper.min.js',
    },
    {
        'src': 'https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/js/bootstrap.min.js',
        'integrity': 'sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy',
        'crossorigin': 'anonymous'
    },
    {
        'src':'https://kit.fontawesome.com/a076d05399.js',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    {
        "href":"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
        "rel":"stylesheet"
    },{
        'href': 'https://fonts.googleapis.com/css?family=Bree Serif',
        'rel': 'stylesheet',
    },{
        'href':'https://fonts.googleapis.com/css?family=Lobster',
        'rel':'stylesheet',
    },{
        'href': 'https://fonts.googleapis.com/css?family=Audiowide|Sofia|Trirong',
        'rel': 'stylesheet',
    },
    {
        'href': 'jquery.datetimepicker.min.css',
        'rel': 'stylesheet',
    },
    {
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi',
        'crossorigin': 'anonymous'
    }
]

app = Dash(__name__,external_scripts=external_scripts,external_stylesheets=external_stylesheets,meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,use-scalable=no'}])

app.head = [html.Link(rel='stylesheet', href='./assets/uidai_style.css')]

server=app.server
app.config.suppress_callback_exceptions=True
app.scripts.config.serve_locally=True
app.title="SANOFI DASHBOARD"

server.config.update(SECRET_KEY="randompossibleocatcthiskyindigout",
    SQLALCHEMY_DATABASE_URI="sqlite:///users.db",
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

db.init_app(server)

#Seeting up the Login Manager for Server
login_manager=LoginManager()
login_manager.init_app(server)
login_manager.login_view='/login'

#Callback to Load the user object
@login_manager.user_loader
def load_user(user_id):
    # m1=session.query(User_1).filter(User_1.id==int(user_id)).first()
    n1=session.query(User_1).filter(User_1.id==int(user_id))
    kk1=''
    for n in n1:
        kk1=n
    # return (session.query(User_1).filter(User_1.id==int(user_id)))
    return kk1
