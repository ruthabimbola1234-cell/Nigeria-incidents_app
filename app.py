import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
# import plotly.express as px
import altair as alt
import re
import os

def load_data():
    # using pandas to load the dataset
    df = pd.read_csv("incidents.csv")
    # add new columns
    incident_list = []
    location_list = []
    for value in df['Title'].astype(str):
      # list comprehension
      parts = [p.strip() for p in re.split(r'[,\.\-]\s*',value) if p.strip()]
      if len(parts) > 1:
           incident_list.append(parts[0])
           location_list.append(parts[-1])
      else:
        incident_list.append(parts[0])
        location_list.append(None)

    df["incident"] = incident_list
    df["location"] = location_list
    # more cleaning ops
    # convert dates
    df["year"] = df['End date'].str.split("-",n=1,expand=True)[0]
    return df

    return df

def main():
    df = load_data()
    st.title("Nigeria Incidents App 2025")
    st.write(df.head(5))

    
    # filters 
    # create filters 
    filters = {
        "incident" : df["incident"].unique(),
        "location" : df["location"].unique(),
        "year" : df["year"].unique()
    }
    # user selection 
    selected_filters = {}

    # generate multi-select widgets dynamically
    for key, options in filters.items():
        selected_filters[key]=st.sidebar.multiselect(key,options)
          
    # parse the filtered content into the dataframe
    df = df.copy()

    # apply filtered selection to the data 

    for key, selected_values in selected_filters.items():
        if selected_values:
            df = df[df[key].isin(selected_values)]

    # metrics


    st.subheader("Summary section")
    # calculations
    no_of_incidents = df.shape[0]
    no_of_deaths = df["Number of deaths"].sum()

    # columns
    col1, col2 =st.columns(2)
    with col1:
        st.metric("No of incidents",no_of_incidents)

    with col2:
        st.metric("No of Deaths", no_of_deaths)




    st.subheader("incidents value counts")
    temp1 = df.incident.value_counts().reset_index()
    st.dataframe(temp1)


    # altair plotting library 
    # bar chart 
    # data for bar chart top 10
    temp1 = temp1.nlargest(10,'count')
    
    chart1 = alt.Chart(temp1).mark_bar().encode(
        x=alt.X('count:Q', title="Incident Count"),
        y=alt.Y('incident:N', sort='-x'),
    ).properties(height=600)

    # display the chart
    st.altair_chart(chart1)

    # chart on deaths
    temp2 = df.groupby('location')['Number of deaths'].sum().reset_index()

    temp2 = temp2.nlargest(10, 'Number of deaths')
    temp2.sort_values(by='Number of deaths',ascending=True)

    # st.dataframe(temp2)

    chart2 = alt.Chart(temp2).mark_bar().encode(
        x=alt.X('Number of deaths:Q', title="Deaths"),
        y=alt.Y('location:N', sort='-x'),
        color=alt.Color("location:N", legend=None)
    ).properties(height=600)

    st.altair_chart(chart2)








    st.write(temp1)







if __name__ == "__main__":
    main()




