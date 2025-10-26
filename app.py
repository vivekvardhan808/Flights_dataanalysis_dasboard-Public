import streamlit as st
import pandas as pd
from plotly import graph_objects as go
from dbhelper import DB #Connecting to the dbhelper file


db = DB()

st.sidebar.title('Flight Analytics')
user_option = st.sidebar.selectbox('Menu',['About Project','Check Flights','Analytics'])

# Check FLights slide
if user_option == 'Check Flights':
    st.markdown("<h1 style='color: #AC94F4;'>Check Flights</h1>", unsafe_allow_html=True)

    # creating two columns
    col1,col2 = st.columns(2)
    
    with col1:
        Source_city = db.fetch_city_names_s()
        Source = st.selectbox('Source',sorted(Source_city))

    with col2:
        Destination_city = db.fetch_city_names_d()
        Destination = st.selectbox('Destination',sorted(Destination_city))

    if st.button('Search'):
        results = db.fetch_all_fights(Source,Destination)  # result of dataframe of flight details
        #avg_price = db.avg_price(Source,Destination)
        kpi_result = db.count_of_fights(Source,Destination)
        custom_column_names = ['Airline','Class','No. of Flights','Avg Price']
        df = pd.DataFrame(results,columns=custom_column_names)

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            pass
        with col2:
            pass
            #st.metric(label="Avg. Price", value=avg_price)
        with col3:
            pass
        with col4:
            st.metric(label="Total No. of FLights", value=kpi_result)
        st.dataframe(df,height=600, width=800)
    
# Analytics Page     
elif user_option == 'Analytics':

    st.markdown("<h1 style='color: #AC94F4;'>Flights Analytics</h1>", unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    
    with col1:

        airline,freq = db.fetch_airline_frequency()
            
        # Create a Plotly pie chart
        # User-defined color palette
        color_palette = ['#240046','#3C096C','#5A189A','#7B2CBF','#9D4EDD','#C77DFF']
        fig = go.Figure(data=[go.Pie(labels=airline,
                                        values=freq,
                                        hoverinfo='label+percent',
                                        marker=dict(colors=color_palette),
                                        textinfo='value')])
        # Customize figure layout
        fig.update_layout(
            title="Airline Frequency Distribution",
            showlegend=False,
            width=400,  # Set the width of the figure
            height=400  # Set the height of the figure
)
        fig.update_traces(textposition='inside', textinfo='percent+label')

        #st.markdown(" ### Airline Distribution")
        # Show the pie chart in Streamlit
        st.plotly_chart(fig)
    
    with col2:
        airport,freq = db.fetch_airport_frequency()
        # Create a Plotly bar chart
        color_scale = ['#240046','#3C096C','#5A189A','#7B2CBF','#9D4EDD','#C77DFF']

        fig = go.Figure(data=[go.Bar(x=airport, y=freq, marker=dict(color=color_scale))])
        fig.update_layout(
            title='Busiest Airport',
            xaxis_title='Airport',
            yaxis_title='Frequency',
            width=400,
            height=400
        )

        # Display the chart in Streamlit
        st.plotly_chart(fig)

    #Fetching hte details from database
    airline,price = db.fetch_avg_price_by_airline()
    # Create a line graph using Plotly Graph Objects
    fig = go.Figure(data=go.Scatter(x=airline, y=price, mode='lines+markers',line=dict(color='#AC94F4')))

    # Set the title and axis labels
    fig.update_layout(
        title='Price Trend Over Airlines',
        xaxis_title='Days',
        yaxis_title='Price',
        width=400,
        height=400
    )

    # Display the graph
    st.plotly_chart(fig,use_container_width=True)

    # Grouped Bar Graphs
    # Fetching data
    s_city,s_count = db.fetch_count_of_flights_source()
    d_city,d_count = db.fetch_count_of_flights_destination()

    color_palette_source = '#3C096C' 
    color_palette_dist = '#9D4EDD'

    # Graph Plotting
    fig = go.Figure()
    fig.add_trace(go.Bar(x=s_city, y=s_count, name='Departing',marker=dict(color=color_palette_source)))
    fig.add_trace(go.Bar(x=s_city, y=d_count, name='Arriving',marker=dict(color=color_palette_dist)))

    # Set the title and axis labels
    fig.update_layout(
        title='Number of flights departing from each source city and arriving at each destination city.',
        xaxis_title='Airport',
        yaxis_title='# of Flights'
    )
    # Display the graph
    st.plotly_chart(fig,use_container_width=True)

    # Fetching data
    data = db.fetch_price_vs_dep_time()

    # Convert data to a pandas DataFrame
    df = pd.DataFrame(data, columns=["Time", "Airline", "Value"])
    # Pivot the data to create a heatmap-ready format
    heatmap_data = df.pivot(index="Airline", columns="Time", values="Value")
    
    # Create the heatmap figure
    heatmap_fig = go.Figure(data=go.Heatmap(
                    z=heatmap_data.values,
                    x=heatmap_data.columns,
                    y=heatmap_data.index,
                    colorscale='Purples'))

    # Customize layout
    heatmap_fig.update_layout(
        title='Airline Traffic Heatmap',
        xaxis_title='Time of Day',
        yaxis_title='Airline'
    )

    st.plotly_chart(heatmap_fig,use_container_width=True)
else:
    # about project page
    st.markdown("<h1 style='color: #AC94F4;'>Flights Data Analysis Dashboard!</h1>", unsafe_allow_html=True)
    st.markdown("Welcome to the Flight Data Analysis Dashboard, where we explore fascinating insights into the flights operating in India! This project aims to provide a comprehensive analysis of various aspects of flights, including airlines, ticket prices, and routes, to help users gain valuable insights and make informed decisions.")

    st.markdown("### Objective")
    st.markdown("The primary objective of this project is to analyze the vast dataset of flight information to uncover interesting patterns, trends, and correlations. By visualizing and exploring this data, we aim to provide a user-friendly interface for understanding key factors that influence flight operations and ticket pricing in India.")

    st.markdown("### Data Source:")
    st.markdown("The flight data used in this analysis is sourced from reliable and up-to-date aviation databases. It includes a wide range of attributes, such as airline details, flight class, ticket prices, source, destination, and more. This extensive dataset is continually updated to ensure accuracy and relevance.")

    st.markdown("Dataset Link : https://www.kaggle.com/datasets/dhirajbembade/indian-airlines-ticket-price-analysis")

    st.markdown("### Dashboard Features:")
    st.markdown("1. **About Project:** This section provides an overview of the project, its objectives, and data sources. Users can learn more about the methodology used in analyzing the flight data and the scope of insights provided.")
    st.markdown("2. **Flights Details:** Here, users can explore the details of all available flights. By selecting a specific source and destination, the dashboard will display relevant information, including the airline name, flight class, and average ticket price. This feature enables users to compare and analyze flight options based on their preferences.")
    st.markdown("3. **Analysis:** The analysis section presents interactive visualizations and charts, highlighting key trends and patterns found in the flight data. Users can interact with various graphs to explore factors influencing ticket prices, popular airlines, busy flight routes, and much more.")

    st.markdown("### Disclaimer:")
    st.markdown("The insights and visualizations presented in this dashboard are for informational and illustrative purposes only. While we strive for accuracy and reliability, we cannot guarantee the absolute correctness of the data. Users are advised to use their discretion and corroborate information from other sources when making any critical decisions based on the insights presented in this dashboard.")

    st.markdown("For any queries or support, please feel free to contact us via the provided contact information. **Happy exploring!**")
