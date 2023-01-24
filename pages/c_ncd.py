import dash
import datetime
from datetime import date
from dash import html, dcc
from dash import Dash, dash_table
import pandas as pd
import pandas
from updated_date import Current_things
from collections import OrderedDict
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

obj_datepicker_ncd=Current_things()

df_ncd=pd.DataFrame()

# ncd_cummulative['HYpertension'].sum()+ncd_cummulative['Diabetes'].sum()+ncd_cummulative['HTN & DM']

df_column_ncd = pd.DataFrame({'Location':pd.Series(dtype='str'),
                        'Hypertension': pd.Series(dtype='int'),
                        'Diabetes': pd.Series(dtype='int'),
                        'Hypertension & Diabetes': pd.Series(dtype='int'),
                        })

def layout():
    return html.Div([
    html.Div([html.P("Non Communicable Diseases")],className='ncd_title',style={"margin-left":"26%","margin-top":"3%","border":"2px double black","border-radius":"8px","width":"46%","text-align":'center',"font-size":"x-large","color":"black","font-family":"serif","font-weight":"700","background-color":"#d9dae0","padding-top":"3px"}),
    html.Div([
    html.Div(dcc.DatePickerRange(id='my_date_picker_range_ncd',display_format='D-M-Y',min_date_allowed=date(2022, 2, 3),max_date_allowed=obj_datepicker_ncd.current_date(),initial_visible_month=date(2022, 2, 3),start_date=date(2022, 2, 3),end_date=obj_datepicker_ncd.current_date(),style={"position":"relative","display":"inline-block","width":"110%","border-radius":"39px","margin-left":"115%","margin-top":"5%","margin-bottom":"7%"}),style={}),
    html.A([html.P("Home",style={})],href='/',style={"border":"2px double black","margin-left":"41%","border-radius":"8px","width":'4%',"height":"3%","padding":"6px","margin-top":"1.5%","background-color":"rgb(215, 215, 215)"}),
    html.A([html.I(className="fa fa-refresh",style={})],href=dash.page_registry['pages.c_ncd']['path'],style={"width":"4%","height":"2.3rem","margin-left":"0.8rem","margin-top":"1.5%","text-align":"center","font-size":"22px","background-color":"rgb(215,215,215)","border-radius":"8px","padding-top":"0.3rem","border":"2px double black"})
    ],style={'display':'flex','flex-direction':'row',"margin-bottom":'-23px'}),
    html.Div([html.Div(id="c_ncd_error",className="ncd_error",style={"width":"70%","height":"1.5rem","margin-left":"20%","margin-top":"3px","font-family":"ui-sans-serif","font-size":"medium"})],style={}),
    dash_table.DataTable(columns=[{'id': c, 'name': c} for c in df_column_ncd.columns],id="table_ncd",
                        style_cell={'overflow': 'hidden','textOverflow': 'ellipsis','maxWidth': '50%','textAlign': 'center'},
                        style_cell_conditional=[{'if': {'column_id': c},'textAlign': 'left'} for c in ['Date', 'Region']],
                        style_data={'color': 'black','backgroundColor': 'white'},
                        style_table={"width":"606px","margin-left":"25%","margin-bottom":"4%"},
                        style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(220, 220, 220)'}],
                        style_header={'backgroundColor': 'rgb(210, 210, 210)','color': 'black','fontWeight': 'bold'}),
        dcc.Interval(
            id='interval-component',
            interval=5*60*1000, # updates in every 5 Minutes
            n_intervals=20
        )
])
    
@app.callback(Output('table_ncd','data'),Output('c_ncd_error','children'),
    inputs=dict(start_date=Input('my_date_picker_range_ncd','start_date'),end_date=Input('my_date_picker_range_ncd','end_date')))
def update_clinic_selected(start_date,end_date):
    start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end =  datetime.datetime.strptime(end_date, '%Y-%m-%d')
    # df_yesterday=df[df['Date']==yesterday]
    
    #If start Date > end Date Values ,Then taking Default Values from 01/11/2022 to till date   
    if start>end:
        return dash.no_update,"Start: {} date is Greater Than End: {} Date Values..!".format(start,end)
        # df_ncd_init=df[(df['Date']>=st) & (df['Date']<=today)]
        # df_ncd_hypertension_initial=pd.DataFrame(df_ncd_init.groupby(['Location'])['HYpertension'].sum()).reset_index()
        # df_ncd_Diabetes_and_owner_initial=pd.DataFrame(df_ncd_init.groupby(['Location'])['Diabetes'].sum()).reset_index()
        # df_ncd_htn_and_cd_initial=pd.DataFrame(df_ncd_init.groupby(['Location'])['HTN & DM'].sum()).reset_index()
        # df_ncd['Location']=df_ncd_hypertension_initial['Location']
        # df_ncd['Hypertension']=df_ncd_hypertension_initial['HYpertension']
        # df_ncd['Diabetes']=df_ncd_Diabetes_and_owner_initial['Diabetes']
        # df_ncd['Hypertension & Diabetes']=df_ncd_htn_and_cd_initial['HTN & DM']
        # return df_ncd.to_dict('records'),"Start: {} date is Greater Than End: {} Date Values..!".format(start,end)
    elif start==end:
        df_ncd_init=df[df['Date']==start]
        df_ncd_hypertension_initial=pd.DataFrame(df_ncd_init.groupby(['Location'])['HYpertension'].sum()).reset_index()
        df_ncd_Diabetes_and_owner_initial=pd.DataFrame(df_ncd_init.groupby(['Location'])['Diabetes'].sum()).reset_index()
        df_ncd_htn_and_cd_initial=pd.DataFrame(df_ncd_init.groupby(['Location'])['HTN & DM'].sum()).reset_index()
        df_ncd['Location']=df_ncd_hypertension_initial['Location']
        df_ncd['Hypertension']=df_ncd_hypertension_initial['HYpertension']
        df_ncd['Diabetes']=df_ncd_Diabetes_and_owner_initial['Diabetes']
        df_ncd['Hypertension & Diabetes']=df_ncd_htn_and_cd_initial['HTN & DM']
        return df_ncd.to_dict('records')," "
    elif start<end:
        df_ncd_init=df[(df['Date']>=start) & (df['Date']<=end)]
        df_ncd_hypertension_initial=pd.DataFrame(df_ncd_init.groupby(['Location'])['HYpertension'].sum()).reset_index()
        df_ncd_Diabetes_and_owner_initial=pd.DataFrame(df_ncd_init.groupby(['Location'])['Diabetes'].sum()).reset_index()
        df_ncd_htn_and_cd_initial=pd.DataFrame(df_ncd_init.groupby(['Location'])['HTN & DM'].sum()).reset_index()
        df_ncd['Location']=df_ncd_hypertension_initial['Location']
        df_ncd['Hypertension']=df_ncd_hypertension_initial['HYpertension']
        df_ncd['Diabetes']=df_ncd_Diabetes_and_owner_initial['Diabetes']
        df_ncd['Hypertension & Diabetes']=df_ncd_htn_and_cd_initial['HTN & DM']
        return df_ncd.to_dict('records')," "