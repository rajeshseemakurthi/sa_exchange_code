import dash
import datetime
from datetime import date
from dash import html, dcc
from dash import Dash, dash_table
import pandas as pd
import pandas
from collections import OrderedDict
from updated_date import Current_things
from pandas._libs.tslibs.timestamps import Timestamp
from dash import html, dcc, callback, Input, Output

#Local Imports
from data_reading import Data_Reading
from server import app

df_main=Data_Reading()
df=df_main.df

st = Timestamp('2022-11-01 00:00:00')
# st = Timestamp('2022-11-01 00:00:00', freq='MS')
st = st.to_pydatetime()
today = pd.to_datetime(date.today(), format='%Y-%m-%d')
yesterday = today-pd.Timedelta(days=1)

start_clinic=Timestamp('2022-10-15 00:00:00')
# start_clinic=Timestamp('2022-10-15 00:00:00', freq='MS')
end_clinic=Timestamp('2022-11-05 00:00:00')
# end_clinic=Timestamp('2022-11-05 00:00:00', freq='MS')

#Empty DataFrame for df['Total Beneficiaries taken Lab tests']
df_cd=pd.DataFrame()

obj_datepicker_mp=Current_things()

df_column_clinic = pd.DataFrame({'Location':pd.Series(dtype='str'),
                        'Common Diseases-Yesterday Count': pd.Series(dtype='int'),
                        'Common Diseases-Cumulative Count': pd.Series(dtype='int')})

def layout():
    return html.Div([
    html.Div([html.P("Common Diseases")],className='cd_title',style={"margin-left":"26%","margin-top":"3%","border":"2px double black","border-radius":"8px","width":"46%","text-align":'center',"font-size":"x-large","color":"black","font-family":"serif","font-weight":"700","background-color":"#d9dae0","padding-top":"3px"}),
    html.Div([
    html.Div(dcc.DatePickerRange(id='my_date_picker_range_mp',display_format='D-M-Y',min_date_allowed=date(2022, 2, 3),max_date_allowed=obj_datepicker_mp.current_date(),initial_visible_month=date(2022, 2, 3),start_date=date(2022, 2, 3),end_date=obj_datepicker_mp.current_date(),style={"position":"relative","display":"inline-block","width":"110%","border-radius":"39px","margin-left":"115%","margin-top":"5%","margin-bottom":"7%"}),style={}),
    html.A([html.P("Home",style={})],href='/',style={"border":"2px double black","margin-left":"41%","border-radius":"8px","width":'4%',"height":"3%","padding":"6px","margin-top":"1.5%","background-color":"rgb(215, 215, 215)"}),
    html.A([html.I(className="fa fa-refresh",style={})],href=dash.page_registry['pages.c_mp']['path'],style={"width":"4%","height":"2.3rem","margin-left":"0.8rem","margin-top":"1.5%","text-align":"center","font-size":"22px","background-color":"rgb(215,215,215)","border-radius":"8px","padding-top":"0.3rem","border":"2px double black"})
    ],style={'display':'flex','flex-direction':'row',"margin-bottom":'-23px'}),
    html.Div([html.Div(id="c_cd_error",className="cd_error",style={"width":"70%","height":"1.5rem","margin-left":"20%","margin-top":"3px","font-family":"ui-sans-serif","font-size":"medium"})],style={}),
    dash_table.DataTable(columns=[{'id': c, 'name': c} for c in df_column_clinic.columns],id="table_cd",
                        style_cell={'overflow': 'hidden','textOverflow': 'ellipsis','maxWidth': '50%','textAlign': 'center'},
                        style_cell_conditional=[{'if': {'column_id': c},'textAlign': 'left'} for c in ['Date', 'Region']],
                        style_data={'color': 'black','backgroundColor': 'white'},
                        style_table={"width":"606px","margin-left":"21%","margin-bottom":"4%"},
                        style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(220, 220, 220)'}],
                        style_header={'backgroundColor': 'rgb(210, 210, 210)','color': 'black','fontWeight': 'bold'}),
        dcc.Interval(
            id='interval-component',
            interval=5*60*1000, # updates in every 5 Minutes
            n_intervals=20
        )
])
    
@app.callback(Output('table_cd','data'),Output('c_cd_error','children'),
    inputs=dict(start_date=Input('my_date_picker_range_cd','start_date'),end_date=Input('my_date_picker_range_cd','end_date')))
def update_clinic_selected(start_date,end_date):
    start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end =  datetime.datetime.strptime(end_date, '%Y-%m-%d')
    df_yesterday=df[df['Date']==yesterday]
    
    #If start Date > end Date Values ,Then taking Default Values from 01/11/2022 to till date   
    if start>end:
        return dash.no_update,"Start: {} date is Greater Than End: {} Date Values..!".format(start,end)
        # df_cd_init=df[(df['Date']>=st) & (df['Date']<=today)]
        # df_cd_initial=pd.DataFrame(df_cd_init.groupby(['Location'])['CD'].sum()).reset_index()
        # df_cd['Location']=df_cd_initial['Location']
        # cd_n1=[]
        # if (df_yesterday.empty)==True:
        #     for i in range(len(df_cd_initial)):
        #         cd_n1.append(0)
        #     df_cd['Common Diseases-Yesterday Count']=cd_n1
        # elif (df_yesterday.empty)!=True:
        #     df_ye=df[df['Date']==yesterday]
        #     df_yest=pd.DataFrame(df_ye.groupby(['Location'])['CD'].sum()).reset_index()
                                                                                                            
        #     mk1=list(df_cd_initial['Location'])
        #     #for #ben to Drug Prescribed Cumulative Yesterday Count Column
        #     df_yeste_fe=df_yest.groupby('Location')['CD'].sum()
        #     df_yester_ma=df_yeste_fe.to_dict()            
            
        #     df_cd_dict={}  #Creating empty Dataframe
        #     for i in range(len(mk1)):
        #         if mk1[i] in df_yester_ma.keys():
        #             df_cd_dict[mk1[i]]=df_yester_ma[mk1[i]]
        #         elif mk1[i] not in df_yester_ma.keys():
        #             df_cd_dict[mk1[i]]=0
        #     df_cd_dict
        #     df_cd_dict_impo=pd.DataFrame.from_dict(df_cd_dict,orient ='index').reset_index()
        #     #Joining above processed Dataframe to df_ref['Referrals-Yesterday Count']
        #     df_cd['Common Diseases-Yesterday Count']=df_cd_dict_impo[0]
        # else:
        #     print("I am in else loop-DOWNSTEP.CD..!") 
        # df_cd['Common Diseases-Cumulative Count']=list(df_cd_initial['CD'])
        # return df_cd.to_dict('records'),"Start: {} date is Greater Than End: {} Date Values..!".format(start,end)
    elif start==end:
        df_cd_init=df[df['Date']==start]
        df_cd_initial=pd.DataFrame(df_cd_init.groupby(['Location'])['CD'].sum()).reset_index()
        df_cd['Location']=df_cd_initial['Location']
        cd_n1=[]
        if (df_yesterday.empty)==True:
            for i in range(len(df_cd_initial)):
                cd_n1.append(0)
            df_cd['Common Diseases-Yesterday Count']=cd_n1
        elif (df_yesterday.empty)!=True:
            df_ye=df[df['Date']==yesterday]
            df_yest=pd.DataFrame(df_ye.groupby(['Location'])['CD'].sum()).reset_index()
                                                                                                            
            mk1=list(df_cd_initial['Location'])
            #for #ben to Drug Prescribed Cumulative Yesterday Count Column
            df_yeste_fe=df_yest.groupby('Location')['CD'].sum()
            df_yester_ma=df_yeste_fe.to_dict()            
            
            df_cd_dict={}  #Creating empty Dataframe
            for i in range(len(mk1)):
                if mk1[i] in df_yester_ma.keys():
                    df_cd_dict[mk1[i]]=df_yester_ma[mk1[i]]
                elif mk1[i] not in df_yester_ma.keys():
                    df_cd_dict[mk1[i]]=0
            df_cd_dict
            df_cd_dict_impo=pd.DataFrame.from_dict(df_cd_dict,orient ='index').reset_index()
            #Joining above processed Dataframe to df_ref['Referrals-Yesterday Count']
            df_cd['Common Diseases-Yesterday Count']=df_cd_dict_impo[0]
        else:
            print("I am in else loop-DOWNSTEP.CD..!") 
        df_cd['Common Diseases-Cumulative Count']=list(df_cd_initial['CD'])
        return df_cd.to_dict('records')," "
    elif start<end:
        df_cd_init=df[(df['Date']>=start) & (df['Date']<=end)]
        df_cd_initial=pd.DataFrame(df_cd_init.groupby(['Location'])['CD'].sum()).reset_index()
        df_cd['Location']=df_cd_initial['Location']
        cd_n1=[]
        if (df_yesterday.empty)==True:
            for i in range(len(df_cd_initial)):
                cd_n1.append(0)
            df_cd['Common Diseases-Yesterday Count']=cd_n1
        elif (df_yesterday.empty)!=True:
            df_ye=df[df['Date']==yesterday]
            df_yest=pd.DataFrame(df_ye.groupby(['Location'])['CD'].sum()).reset_index()
                                                                                                            
            mk1=list(df_cd_initial['Location'])
            #for #ben to Drug Prescribed Cumulative Yesterday Count Column
            df_yeste_fe=df_yest.groupby('Location')['CD'].sum()
            df_yester_ma=df_yeste_fe.to_dict()            
            
            df_cd_dict={}  #Creating empty Dataframe
            for i in range(len(mk1)):
                if mk1[i] in df_yester_ma.keys():
                    df_cd_dict[mk1[i]]=df_yester_ma[mk1[i]]
                elif mk1[i] not in df_yester_ma.keys():
                    df_cd_dict[mk1[i]]=0
            df_cd_dict
            df_cd_dict_impo=pd.DataFrame.from_dict(df_cd_dict,orient ='index').reset_index()
            #Joining above processed Dataframe to df_ref['Referrals-Yesterday Count']
            df_cd['Common Diseases-Yesterday Count']=df_cd_dict_impo[0]
        else:
            print("I am in else loop-DOWNSTEP.CD..!") 
        df_cd['Common Diseases-Cumulative Count']=list(df_cd_initial['CD'])
        return df_cd.to_dict('records')," "