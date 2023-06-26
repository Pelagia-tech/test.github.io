import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go



st.set_page_config(page_title="Marketplace Dashboard",layout="wide")
df=pd.read_excel("Superstore.xlsx")
df['Order_Date'] = pd.to_datetime(df['Order_Date']).dt.strftime('%Y-%m-%d')
df.sort_values(by='Order_Date',ascending=False)


rad=st.sidebar.radio("Joina manager",{"Home","Sales"})
rad2=st.sidebar.radio("Managers",{"Inventory","Marketing "})

if rad=="Home":
    st.title("Marketplace Dashboard")
   
    df2=df.groupby(["Order_Date","Customer_Name"],as_index=False).sum()  
    date_filter=st.selectbox("Select the date you want", df["Order_Date"].unique())
   
    selection=df2.query("Order_Date==@date_filter")

    #st.subheader("Aggregate values")
    kpi1,kpi2,kpi3=st.columns(3)
    kpi1.metric(label="Traffic on Homepage", value=selection["Traffic_On_Home_Page"].sum().round())
    kpi2.metric(label="Total_Orders", value=selection["Total_Orders"].sum().round())
    kpi3.metric(label="Failed_Orders", value=selection["Failed_Orders"].sum().round())

    kp1,kp2,kp3=st.columns(3)
    kp1.metric("Customers", value=selection["Customer_Name"].count())
    kp2.metric("Revenue", value=selection["Sales"].sum().round())
    kp3.metric(label="Profit", value=selection["Profit"].sum().round())

    df3=df.groupby(["Sub_Category","Order_Date"], as_index=False).sum()
    st.plotly_chart(px.scatter(df3,x="Traffic_On_Home_Page",y="Total_Orders", animation_frame="Order_Date",size="Sales",color="Sub_Category",hover_name="Sub_Category",range_y=[0,400],range_x=[0,1000]))
    #st.plotly_chart(px.scatter(df3,x="Sales",y="Profit", animation_frame="Order_Date",size="Traffic_On_Home_Page",color="Sub_Category",hover_name="Sub_Category",range_y=[0,2000],range_x=[0,1000]))


 
if rad=="Sales":
    st.header("Sales Dashboard")
    #st.subheader("Aggregate values")
    kpi1,kpi2=st.columns(2)
    kpi1.metric(label="Traffic on Homepage", value=df["Traffic_On_Home_Page"].sum().round())
    kpi2.metric("Customers", value=df["Customer_Name"].count())
    kp1,kp2=st.columns(2)
    kp1.metric("Revenue", value=df["Sales"].sum().round())
    kp2.metric(label="Profit", value=df["Profit"].sum().round())
    st.subheader("Graphs of data grouped by Sub_Category")
    df3=df.groupby(["Sub_Category","Order_Date"], as_index=False).sum()
    category=st.sidebar.multiselect(label="Categories",default=df3["Sub_Category"].unique(), options=df3["Sub_Category"].unique())
    sel=df3.query("Sub_Category==@category")
    bar1=px.bar(sel,x="Sub_Category", y="Sales")
    line1=px.scatter(sel,x="Sub_Category", y="Profit", size="Total_Orders", color="Profit")
    left1,right1=st.columns(2)

    left1.plotly_chart(bar1,use_container_width=True)

    right1.plotly_chart(line1,use_container_width=True)

    #st.subheader("Graphs of data grouped by customer names")

    #df4=df.groupby("Customer_Name", as_index=False).sum()

    #customer=st.sidebar.multiselect("Customers", options=df3["Customer_Name"].unique(),default=df3["Customer_Name"].unique())

    #selection3=df4.query("Customer_Name==@customer")

    #st.dataframe(selection3)
    #kpi1=st.columns(1)
    #st.plotly_chart(px.scatter(selection3,x="Customer_Name",y="Sales",size="Sales"))
    #st.plotly_chart(px.line(selection3,x="Customer_Name",y="Sales 


 
if rad2=="Inventory ":
    st.title("Inventory Dashboard")
    st.subheader("Graphs of data grouped by order date")
    kp1,kp2,kp3=st.columns(3)
    kp1.metric("Customers", value=df["Customer_Name"].count())
    kp2.metric(label="Total_Orders", value=int(df["Total_Orders"].sum()))
    kp3.metric(label="Failed_Orders", value=int(df["Failed_Orders"].sum()))


    df2=df.groupby(["Order_Date","Ship_Mode"], as_index=False).sum()

    order=st.sidebar.multiselect("Order_Date",options=df2["Order_Date"].unique(), default=df2["Order_Date"].unique())

    selection2=df2.query("Order_Date==@order")

    #st.dataframe(selection2)

    bar2=px.bar(selection2,x="Order_Date", y="Sales", color="Discount")

    ba=px.bar(selection2,x="Order_Date", y="Total_Orders",color="Ship_Mode")

    #line2=px.line(selection2,x="Order_Date", y="Profit")

    left2,right2=st.columns(2)

    left2.plotly_chart(bar2,use_container_width=True)

    right2.plotly_chart(ba,use_container_width=True)

    #right2.plotly_chart(line2,use_container_width=True)
    


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)