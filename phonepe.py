import streamlit as st
from streamlit_option_menu import option_menu  # for option menu in sidebar
import plotly.express as px
import pandas as pd
import mysql.connector
import json
import requests

# set page configuration
st.set_page_config(layout="wide")

# dataframe creation

mycon = mysql.connector.connect(
    host="localhost",
    user="root",
    password='Mageswari@123',
    database="Phonepe_data",
    auth_plugin='mysql_native_password'
)

mycursor = mycon.cursor()

# aggregate insurance dataframe(Df)
mycursor.execute("SELECT * FROM aggregated_insurance")
table1 = mycursor.fetchall()

# to convert sql table - table1 into a dataframe
Aggregated_insurance = pd.DataFrame(table1, columns=('States', 'Years', 'Quarter', 'Transaction_type', 'Transaction_count',
                                                      'Transaction_amount'))

# aggregate transaction dataframe(Df)
mycursor.execute("SELECT * FROM aggregated_transaction")
table2=mycursor.fetchall()

Aggregated_transaction=pd.DataFrame(table2,columns = ('States', 'Years', 'Quarter', 'Transaction_type', 'Transaction_count',
       'Transaction_amount'))

# aggregate user dataframe(Df)
mycursor.execute("SELECT * FROM aggregated_user")
table3=mycursor.fetchall()

Aggregated_user=pd.DataFrame(table3,columns = ('States', 'Years', 'Quarter', 'Brands', 'Transaction_count',
       'Percentage'))

# map insurance df
mycursor.execute("SELECT * FROM map_insurance")
table4=mycursor.fetchall()

Map_insurance=pd.DataFrame(table4,columns = ('States','Years','Quarter','Districts','Transaction_count','Transaction_amount'))

#map_transaction dataframe
mycursor.execute("SELECT * FROM map_transaction")
table5=mycursor.fetchall()

Map_transaction=pd.DataFrame(table5,columns = ('States', 'Years', 'Quarter', 'Districts', 'Transaction_count',
       'Transaction_amount'))

#map_user dataframe
mycursor.execute("SELECT * FROM map_user")
table6=mycursor.fetchall()

Map_user=pd.DataFrame(table6,columns = ('States', 'Years', 'Quarter', 'Districts', 'RegisteredUser',
       'AppOpens'))

#top_insurance dataframe
mycursor.execute("SELECT * FROM top_insurance")
table7=mycursor.fetchall()

Top_insurance=pd.DataFrame(table7,columns = ('States', 'Years', 'Quarter', 'Pincodes', 'Transaction_count',
       'Transaction_amount'))

# top_transaction dataframe
mycursor.execute("SELECT * FROM top_transaction")
table8=mycursor.fetchall()

Top_transaction=pd.DataFrame(table8,columns = ('States', 'Years', 'Quarter', 'Pincodes', 'Transaction_count',
       'Transaction_amount'))

# top_user
mycursor.execute("SELECT * FROM top_user")
table9=mycursor.fetchall()

Top_user=pd.DataFrame(table9,columns = ('States', 'Years', 'Quarter', 'Pincodes', 'RegisteredUser'))





def Transaction_amount_count_Y(df, year):  # Y-year
    tacy = df[df["Years"] == year]  # to get only 2021 data, tacy-transaction_amount_count_year
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()  # tacyg-grouped data of tacy
    tacyg.reset_index(inplace=True)

    column1, column2 = st.columns(2)
    with column1:
        fig_amount = px.bar(tacyg, x="States", y="Transaction_amount", title=f"{year} Transaction Amount",
                            color_discrete_sequence=px.colors.sequential.Agsunset, height=550, width=500)
        st.plotly_chart(fig_amount)

    with column2:
        fig_count = px.bar(tacyg, x="States", y="Transaction_count", title=f"{year} Transaction Count",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=550, width=500)

        st.plotly_chart(fig_count)

     # geovisualisation (India map)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    #response

    data1=json.loads(response.content)
    #data1                             # gives all the content in that json url

    state_names=[]
    for feature in data1["features"]:
        state_names.append(feature["properties"]["ST_NM"])

    state_names.sort()

    column1,column2=st.columns(2)
    with column1:
        fig_india1=px.choropleth(tacyg,geojson=data1,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="States", title=f"{year} Transaction amount", 
                                fitbounds="locations",height=500,width=500)
        
        fig_india1.update_geos(visible=False) # to remove the boundaries of world map other than india
        st.plotly_chart(fig_india1)

    with column2:
        fig_india2=px.choropleth(tacyg,geojson=data1,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name="States", title=f"{year} Transaction Count", 
                                fitbounds="locations",height=500,width=500)
        
        fig_india2.update_geos(visible=False) # to remove the boundaries of world map other than india
        st.plotly_chart(fig_india2)

    return tacy


def Transaction_amount_count_Y_Q(df,quarter):                            # Y-year
    tacy=df[df["Quarter"] == quarter] # to get only 2021 data, tacy-transaction_amount_count_year
    #tacy['Years'].unique()
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()  #tacyg-grouped data of tacy
    tacyg.reset_index(inplace=True)

    column1,column2=st.columns(2)
    with column1:
        fig_amount=px.bar(tacyg,x="States",y="Transaction_amount",title=f"{tacy['Years'].min()} Year {quarter} Quarter Transaction Amount ",color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width=600)
        st.plotly_chart(fig_amount)

    with column2:
        fig_count=px.bar(tacyg,x="States",y="Transaction_count",title=f"{tacy['Years'].min()} Year {quarter} Quarter Transaction Count ",color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
        st.plotly_chart(fig_count)

    # geovisualisation (India map)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    #response

    data1=json.loads(response.content)
    #data1                             # gives all the content in that json url

    state_names=[]
    for feature in data1["features"]:
        state_names.append(feature["properties"]["ST_NM"])

    state_names.sort()

    column1,column2=st.columns(2)
    with column1:
        fig_india1=px.choropleth(tacyg,geojson=data1,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="States", title=f"{tacy['Years'].min()} Year {quarter} Quarter Transaction amount", 
                                fitbounds="locations",height=500,width=500)
        
        fig_india1.update_geos(visible=False) # to remove the boundaries of world map other than india
        st.plotly_chart(fig_india1)

    with column2:
        fig_india2=px.choropleth(tacyg,geojson=data1,locations="States",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name="States", title=f"{tacy['Years'].min()} Year {quarter} Quarter Transaction Count", 
                                fitbounds="locations",height=500,width=500)
        
        fig_india2.update_geos(visible=False) # to remove the boundaries of world map other than india
        st.plotly_chart(fig_india2)

    return tacy

def AggregateTransaction_transactionType(df,state):

    tacy=df[df["States"]==state]
    tacy.reset_index(drop=True,inplace=True)


    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()  #tacyg-grouped data of tacy
    tacyg.reset_index(inplace=True)

    column1,column2=st.columns(2)
    with column1:
        fig_pie1=px.pie(data_frame=tacyg,names="Transaction_type",
                        values="Transaction_amount",width=500,height=500,title=f"{state}-Transaction Amount",
                        hole=0.5)


        st.plotly_chart(fig_pie1)

    with column2:
        fig_pie2=px.pie(data_frame=tacyg,names="Transaction_type",
                        values="Transaction_count",width=500,height=500,title=f"{state}-Transaction Count",
                        hole=0.5)

        st.plotly_chart(fig_pie2)


# aggregated user analysis

# aguy-aggregated_user year

def AggregateUser_plot1(df,year):
    aguy=df[df["Years"]==year]
    aguy.reset_index(drop=True,inplace=True)

    aguyg=pd.DataFrame(aguy.groupby("Brands")[["Transaction_count"]].sum())
    aguyg.reset_index(inplace=True)


    fig_bar1=px.bar(aguyg,x="Brands",y="Transaction_count",title=f"{year} Brands And Transaction Count",
                    width=1000,color_discrete_sequence=px.colors.sequential.haline_r,
                    hover_name="Brands")

    st.plotly_chart(fig_bar1)


    return aguy

# Aggregated_user Analysis2

def AggregatedUser_plot2(df,quarter):
    aguyq=df[df["Quarter"]==quarter]
    aguyq.reset_index(drop=True,inplace=True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar2=px.bar(aguyqg,x="Brands",y="Transaction_count",title=f"{quarter} Quarter - Brands And Transaction Count",
                    width=1000,color_discrete_sequence=px.colors.sequential.Magma,hover_name="Brands")


    st.plotly_chart(fig_bar2)

    return aguyq

# Aggregated user analysis 3
def AggregatedUser_plot3(df,state):
    auyqs=df[df["States"]==state]
    auyqs.reset_index(drop=True,inplace=True)

    # Pie chart
    fig_pie = px.pie(auyqs, values='Transaction_count', names='Brands',
                     title=f"Transaction count distribution for Brands in {state}",
                     hover_data=["Percentage"],
                     labels={"Brands": "Brands", "Transaction_count": "Transaction Count"},
                     width=800, height=600)

    st.plotly_chart(fig_pie)


# map insurance district

def Map_insurance_District(df,state):

    tacy=df[df["States"]==state]
    tacy.reset_index(drop=True,inplace=True)


    tacyg=tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()  #tacyg-grouped data of tacy
    tacyg.reset_index(inplace=True)

    column1,column2=st.columns(2)
    with column1:
        fig_bar1=px.bar(data_frame=tacyg,x="Transaction_amount",
                        y="Districts",orientation="h",
                        width=600,height=600,title=f"{state}-District And Transaction Amount",color_discrete_sequence=px.colors.sequential.Magenta)

        st.plotly_chart(fig_bar1)

    with column2:

        fig_bar2=px.bar(data_frame=tacyg,x="Transaction_count",
                        y="Districts",orientation="h",
                        width=600,height=600,title=f"{state}-District And Transaction Count",color_discrete_sequence=px.colors.sequential.Mint)

        st.plotly_chart(fig_bar2)

    return tacy


    


# streamlit part

st.title("PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    select = option_menu("Main Menu", ["Home", "Data Exploration"])

if select == "Home":
    pass

elif select == "Data Exploration":
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method = st.radio("Select The Method", ["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":

            column1, column2 = st.columns(2)
            with column1:
                years = st.slider("Select The Year", Aggregated_insurance['Years'].unique().min(),
                                  Aggregated_insurance['Years'].unique().max(), Aggregated_insurance['Years'].unique().min())

            tac_Y=Transaction_amount_count_Y(Aggregated_insurance, years)

            column1,column2=st.columns(2)
            with column1:
                quarters = st.slider("Select The Quarter", tac_Y['Quarter'].unique().min(),
                                    tac_Y['Quarter'].unique().max(), tac_Y['Quarter'].unique().min())
                
            Transaction_amount_count_Y_Q(tac_Y,quarters)

        elif method == "Transaction Analysis":
            
            column1, column2 = st.columns(2)
            with column1:
                years = st.slider("Select The Year", Aggregated_transaction['Years'].unique().min(),
                                  Aggregated_transaction['Years'].unique().max(), Aggregated_transaction['Years'].unique().min())

            Aggregated_transaction_tac_Y=Transaction_amount_count_Y(Aggregated_transaction, years)


            column1,column2=st.columns(2)
            with column1:
                states=st.selectbox("Select The State",Aggregated_transaction_tac_Y["States"].unique())

            AggregateTransaction_transactionType(Aggregated_transaction_tac_Y,states)    

            column1,column2=st.columns(2)
            with column1:
                quarters = st.slider("Select The Quarter", Aggregated_transaction_tac_Y['Quarter'].unique().min(),
                                    Aggregated_transaction_tac_Y['Quarter'].unique().max(), Aggregated_transaction_tac_Y['Quarter'].unique().min())
                
            AggregateTransacation_tac_Y_Q=Transaction_amount_count_Y_Q(Aggregated_transaction_tac_Y,quarters)

            
            column1,column2=st.columns(2)
            with column1:
                states=st.selectbox("Select The State_Type",AggregateTransacation_tac_Y_Q["States"].unique())

            AggregateTransaction_transactionType(AggregateTransacation_tac_Y_Q,states)    




        elif method == "User Analysis":
            column1, column2 = st.columns(2)
            with column1:
                years = st.slider("Select The Year", Aggregated_user['Years'].unique().min(),
                                  Aggregated_user['Years'].unique().max(), Aggregated_user['Years'].unique().min())

            AggregatedUser_year=AggregateUser_plot1(Aggregated_user,years)

            column1,column2=st.columns(2)
            with column1:
                quarters = st.slider("Select The Quarter", AggregatedUser_year['Quarter'].unique().min(),
                                   AggregatedUser_year['Quarter'].unique().max(), AggregatedUser_year['Quarter'].unique().min())
                
                AggregatedUser_year_Q=AggregatedUser_plot2(AggregatedUser_year,quarters)

            column1,column2=st.columns(2)
            with column1:
                states=st.selectbox("Select The State_AggregateUser",AggregatedUser_year_Q["States"].unique())

            AggregatedUser_plot3(AggregatedUser_year_Q,states)    


    with tab2:
        method1 = st.radio("Select The Method", ["Map Insurance", "Map Transaction", "Map User"])

        if method1 == "Map Insurance":
            column1, column2 = st.columns(2)
            with column1:
                years = st.slider("Select The Year", Map_insurance['Years'].unique().min(),
                                Map_insurance['Years'].unique().max(), Map_insurance['Years'].unique().min())

            Map_insurance_tac_Y=Transaction_amount_count_Y(Map_insurance, years)

            column1,column2=st.columns(2)
            with column1:
                states=st.selectbox("Select The State_Mapinsurance",Map_insurance_tac_Y["States"].unique())

            Map_insurance_District(Map_insurance_tac_Y,states)    


            column1,column2=st.columns(2)
            with column1:
                quarters = st.slider("Select The Quarter", Map_insurance_tac_Y['Quarter'].unique().min(),
                                    Map_insurance_tac_Y['Quarter'].unique().max(), Map_insurance_tac_Y['Quarter'].unique().min())
                
            Map_insurance_tac_Y_Q=Transaction_amount_count_Y_Q(Map_insurance_tac_Y,quarters)

            column1,column2=st.columns(2)
            with column1:
                states=st.selectbox("Select The State_MapInsurance",Map_insurance_tac_Y_Q["States"].unique())

            Map_insurance_District(Map_insurance_tac_Y_Q,states)    


        elif method1 == "Map Transaction":
            pass

        elif method1 == "Map User":
            pass

    with tab3:
        method2 = st.radio("Select The Method", ["Top Insurance", "Top Transaction", "Top User"])

        if method2 == "Top Insurance":
            pass

        elif method2 == "Top Transaction":
            pass

        elif method2 == "Top User":
            pass

elif select == "Top Charts":
    pass

