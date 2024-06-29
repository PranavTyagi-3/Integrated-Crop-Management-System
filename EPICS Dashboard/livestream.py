# Make sure to import all necessary modules at the beginning
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import mysql.connector
import requests
from streamlit_option_menu import option_menu

# The first Streamlit command should be `st.set_page_config`
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",  # Set the sidebar to be expanded by default
    page_title="FarmEazy",  # Set the title of the page
    # Optionally set the icon for the page, if applicable
)


@st.cache_data
@st.cache_resource
def load_livestream_data():
    data = pd.read_csv('cropyield.csv')
    return data

def generate_status_card(title, value, background_color='#EFF0F4'):
    card_html = f"""
        <div style="padding: 10px; border: 2px solid #167B24; border-radius: 10px; margin-top: 20px; text-align: center; height: 120px;background-color:{background_color}; margin-bottom: 10px;">
            <h4 style="color: #167B24;", style="font size: 12px">{title}</h4>
            <h4 style="color: #167B24; font-size: 22px;">{value}</h4>
        </div>
    """
    return card_html

def generate_count_card(title, count):
    card_html = f"""
        <div style="padding: 10px; border: 2px solid #167B24; border-radius: 10px; margin-top: 20px; text-align: center;">
            <h4 style="color:#167B24;">{title}</h4>
            <p style="color: #167B24;">{count}</p>
        </div>
    """
    return card_html

# Function to get rice yield for the selected state, district, and years
def get_rice_yield(selected_state, selected_district, selected_years, data):
    filtered_data = data[
        (data['State Name'] == selected_state) &
        (data['Dist Name'] == selected_district) &
        ((data['Year'] >= selected_years[0]) & (data['Year'] <= selected_years[1]))
    ]
    total_rice_yield = filtered_data['RICE YIELD (Kg per ha)'].sum()
    return total_rice_yield

def get_wheat_yield(selected_state, selected_district, selected_years, data):
    filtered_data = data[
        (data['State Name'] == selected_state) &
        (data['Dist Name'] == selected_district) &
        ((data['Year'] >= selected_years[0]) & (data['Year'] <= selected_years[1]))
    ]
    total_rice_yield = filtered_data['WHEAT YIELD (Kg per ha)'].sum()
    return total_rice_yield

def get_kharifsorghum_yield(selected_state, selected_district, selected_years, data):
    filtered_data = data[
        (data['State Name'] == selected_state) &
        (data['Dist Name'] == selected_district) &
        ((data['Year'] >= selected_years[0]) & (data['Year'] <= selected_years[1]))
    ]
    total_kharifsorghum_yield = filtered_data['KHARIF SORGHUM YIELD (Kg per ha)'].sum()
    return total_kharifsorghum_yield

def get_rabisorghum_yield(selected_state, selected_district, selected_years, data):
    filtered_data = data[
        (data['State Name'] == selected_state) &
        (data['Dist Name'] == selected_district) &
        ((data['Year'] >= selected_years[0]) & (data['Year'] <= selected_years[1]))
    ]
    total_rabisorghum_yield = filtered_data['RABI SORGHUM YIELD (Kg per ha)'].sum()
    return total_rabisorghum_yield

# Function to get rice yield for the selected state, district, and years
def get_rice_yield_line(selected_state, selected_district, selected_years, data):
    filtered_data = data[
        (data['State Name'] == selected_state) &
        (data['Dist Name'] == selected_district) &
        ((data['Year'] >= selected_years[0]) & (data['Year'] <= selected_years[1]))
    ]
    fig = go.Figure()
    total_rice_yield = filtered_data['RICE YIELD (Kg per ha)'].sum()
    
    fig.add_trace(go.Scatter(x=filtered_data['Year'], y=filtered_data['RICE YIELD (Kg per ha)'],
                             mode='lines', name='Rice Yield'))

    fig.update_layout(
        title='Rice Yield Over Time',
        xaxis_title='Year',
        yaxis_title='Rice Yield (Kg per ha)',
        showlegend=True,
        plot_bgcolor='#72FF86',
        paper_bgcolor='#EFF0F4',
        autosize=True,
        margin=dict(l=75, r=75, b=75, t=75, pad=75),
    )

    return fig


# Function to get rice production for the selected state, district, and years
def get_rice_production(selected_state, selected_district, selected_years, data):
    filtered_data = data[
        (data['State Name'] == selected_state) &
        (data['Dist Name'] == selected_district) &
        ((data['Year'] >= selected_years[0]) & (data['Year'] <= selected_years[1]))
    ]
    fig=total_rice_production = filtered_data['RICE PRODUCTION (1000 tons)'].sum()
    fig.update_layout({
        'plot_bgcolor': '#167B24',
        'paper_bgcolor': '#EFF0F4',
       
        'autosize': True,
        'margin': {
            'l': 75,
            'r': 75,
            'b': 75,
            't': 75,
            'pad': 75
        },
        'xaxis': {
            'showline': True,
            'title': 'Date'
        },
        'yaxis': {
            'showline': True,
            'title': 'Usage Count'
        }
    }, width=750)

  
    return fig


def get_wheat_yield_line(selected_state, selected_district, selected_years, data):
    filtered_data = data[
        (data['State Name'] == selected_state) &
        (data['Dist Name'] == selected_district) &
        ((data['Year'] >= selected_years[0]) & (data['Year'] <= selected_years[1]))
    ]
    fig = go.Figure()
    total_wheat_yield = filtered_data['WHEAT YIELD (Kg per ha)'].sum()
    
    fig.add_trace(go.Scatter(x=filtered_data['Year'], y=filtered_data['WHEAT YIELD (Kg per ha)'],
                             mode='lines', name='Wheat Yield'))

    fig.update_layout(
        title='Wheat Yield Over Time',
        xaxis_title='Year',
        yaxis_title='Wheat Yield (Kg per ha)',
        showlegend=True,
        plot_bgcolor='#72FF86',
        paper_bgcolor='#EFF0F4',
        autosize=True,
        margin=dict(l=75, r=75, b=75, t=75, pad=75),
    )

    return fig


# Function to get rice production for the selected state, district, and years
def get_wheat_production(selected_state, selected_district, selected_years, data):
    filtered_data = data[
        (data['State Name'] == selected_state) &
        (data['Dist Name'] == selected_district) &
        ((data['Year'] >= selected_years[0]) & (data['Year'] <= selected_years[1]))
    ]
    fig=total_wheat_production = filtered_data['WHEAT PRODUCTION (1000 tons)'].sum()
    fig.update_layout({
        'plot_bgcolor': '#167B24',
        'paper_bgcolor': '#EFF0F4',
       
        'autosize': True,
        'margin': {
            'l': 75,
            'r': 75,
            'b': 75,
            't': 75,
            'pad': 75
        },
        'xaxis': {
            'showline': True,
            'title': 'Date'
        },
        'yaxis': {
            'showline': True,
            'title': 'Usage Count'
        }
    }, width=750)

  
    return fig

# Function to generate HTML for a status card

def get_stacked_bar_chart(selected_state, selected_district, selected_years, data):
    filtered_data = data[
        (data['State Name'] == selected_state) &
        (data['Dist Name'] == selected_district) &
        ((data['Year'] >= selected_years[0]) & (data['Year'] <= selected_years[1]))
    ]

    if filtered_data.empty:
        st.warning("No data available for the selected criteria.")
        return None

    fig = go.Figure()

    rice_yield = filtered_data['RICE YIELD (Kg per ha)'].tolist()
    wheat_yield = filtered_data['WHEAT YIELD (Kg per ha)'].tolist()
    soybean_yield = filtered_data['SOYABEAN YIELD (Kg per ha)'].tolist()

    years = filtered_data['Year'].tolist()

    # Assigning different color hex values for each bar
    rice_color = '#52a447'  # Light Salmon
    wheat_color = '#98FB98'  # Pale Green
    soybean_color = '#cce7c9'  # Sky Blue

    fig.add_trace(go.Bar(
        x=years,
        y=rice_yield,
        name='Rice Yield',
        marker=dict(color=rice_color)
    ))

    fig.add_trace(go.Bar(
        x=years,
        y=wheat_yield,
        name='Wheat Yield',
        marker=dict(color=wheat_color)
    ))

    fig.add_trace(go.Bar(
        x=years,
        y=soybean_yield,
        name='Soybean Yield',
        marker=dict(color=soybean_color)
    ))

    fig.update_layout(
        title=f'Rice, Wheat, and Soybean Yield for {selected_district}, {selected_state} ({selected_years[0]}-{selected_years[1]})',
        xaxis_title='Year',
        yaxis_title='Yield (Kg per ha)',
        barmode='stack'
        
    )

    return fig
def generate_crop_donut_chart(selected_state, selected_district, selected_years,data):
    filtered_data = data[
        (data['State Name'] == selected_state) &
        (data['Dist Name'] == selected_district) &
        ((data['Year'] >= selected_years[0]) & (data['Year'] <= selected_years[1]))
    ]
    
    crop_names = ['Finger Millet', 'BARLEY', 'CHICKPEA', 'PIGEONPEA']
    total_yield = filtered_data[['FINGER MILLET YIELD (Kg per ha)', 'BARLEY YIELD (Kg per ha)',
                        'CHICKPEA YIELD (Kg per ha)', 'PIGEONPEA YIELD (Kg per ha)']].sum()

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=crop_names,
        values=total_yield,
        hole=0.4,
        marker=dict(colors=['#52a447', '#98FB98', '#023603','#cce7c9']),  # Customizing colors
        
       
        textinfo='percent+label',
    ))

    fig.update_layout(
        title='Crop Yield Distribution',
        showlegend=True,
        legend=dict(title='Crops'),
    )

    return fig

def get_crop_yield_line(selected_state, selected_district, selected_years, data, crop_names):
    filtered_data = data[
        (data['State Name'] == selected_state) &
        (data['Dist Name'] == selected_district) &
        ((data['Year'] >= selected_years[0]) & (data['Year'] <= selected_years[1]))
    ]

    fig = go.Figure()

    # Define custom colors for each crop
    color_dict = {
        'SAFFLOWER': '#52a447', 
        'RAPESEED AND MUSTARD': '#98FB98',  
        'CASTOR': '#023603',  
        'LINSEED': '#cce7c9'  
    }
    
    
    for crop_name in crop_names:
        crop_yield_column = f'{crop_name} YIELD (Kg per ha)'
        total_crop_yield = filtered_data[crop_yield_column].sum()

        # Use custom color for each crop
        line_color = color_dict.get(crop_name, '#000000')  # Default to black if color not specified

        fig.add_trace(go.Scatter(
            x=filtered_data['Year'],
            y=filtered_data[crop_yield_column],
            mode='lines',
            name=f'{crop_name} Yield',
            line=dict(color=line_color)
        ))

    fig.update_layout(
        title=f'Crop Yield Over Time ({", ".join(crop_names)})',
        xaxis_title='Year',
        yaxis_title='Crop Yield (Kg per ha)',
        showlegend=True,
        #plot_bgcolor='#EFF0F4',
        #paper_bgcolor='#EFF0F4',
        autosize=True,
        margin=dict(l=75, r=75, b=75, t=75, pad=75),
    )

    return fig

def get_kharif_rabi_sorghum_yield(selected_state, selected_district, selected_years, data):
    filtered_data = data[
        (data['State Name'] == selected_state) &
        (data['Dist Name'] == selected_district) &
        ((data['Year'] >= selected_years[0]) & (data['Year'] <= selected_years[1]))
    ]

    fig = go.Figure()

    kharif_sorghum_yield = filtered_data['KHARIF SORGHUM YIELD (Kg per ha)']
    rabi_sorghum_yield = filtered_data['RABI SORGHUM YIELD (Kg per ha)']
    years = filtered_data['Year']

    # Specific hex codes for the line colors
    kharif_color = '#52a447'  # Light Salmon
    rabi_color = '#023603'  # Sky Blue

    fig.add_trace(go.Scatter(x=years, y=kharif_sorghum_yield, mode='lines', name='Kharif Sorghum Yield', line=dict(color=kharif_color)))
    fig.add_trace(go.Scatter(x=years, y=rabi_sorghum_yield, mode='lines', name='Rabi Sorghum Yield', line=dict(color=rabi_color)))

    fig.update_layout(
        title=f'Kharif vs Rabi Sorghum Yield for {selected_district}, {selected_state} ({selected_years[0]}-{selected_years[1]})',
        xaxis_title='Year',
        yaxis_title='Yield (Kg per ha)',
        showlegend=True,
        autosize=True,
        margin=dict(l=75, r=75, b=75, t=75, pad=75),
    )

    return fig


def app():
    data = load_livestream_data()

    custom_css = """
        <style>
          .st-cc {
            border-radius: 5px;
            overflow: hidden;
          }
          .stSelectbox {
            border-radius: 5px;
            overflow: hidden;
          }
          .st-ke {
            font-size: 50px !important;  
          }

          /* Add custom styling for the selected_years slider */
          .selected-years-container {
            color: #cce7c9;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
          }

          /* Customize the slider handle and track color */
          .selected-years-container .stSlider .stSlider-handle {
            background-color: #cce7c9!important; /* Green color */
          }
          .selected-years-container .stSlider .stSlider-track {
            background-color: #cce7c9 !important; /* Green color */
          }
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background-color: #EFF0F4; padding: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); margin-top:0px;margin-bottom: 30px;">
          <h1 style="color: #167B24;">FarmEazy</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
    home_page_url = "http://example.com"  # Update with your desired URL or Streamlit page
    st.markdown(
        f"<a href='{home_page_url}' target='_self' style='float:right;'>Back to Home</a>",
        unsafe_allow_html=True,
    )
    
    col1, col2, col3 = st.columns([2, 2, 2])
    with col2:
        selected_state = st.selectbox("Select State", data['State Name'].unique(), key='dropdown_plotly1')

        # Filter the DataFrame based on the selected state
        filtered_districts = data[data['State Name'] == selected_state]

    with col3:
        selected_district = st.selectbox("Select District", filtered_districts['Dist Name'].unique(), key='dropdown_plotly2')
    
    with col1:
        selected_years = st.slider("Select Years", 2000, 2017, (2000, 2017))

  

    col4, col5, col6, col7 = st.columns([2, 2, 2, 2])
    with col4:
        total_rice_yield = get_rice_yield(selected_state, selected_district, selected_years, data)

        riceyield_card_html = generate_status_card("Total Rice Yield", f"{total_rice_yield:.2f}")
        st.markdown(riceyield_card_html, unsafe_allow_html=True)
        

    with col5:
        total_wheat_yield = get_wheat_yield(selected_state, selected_district, selected_years, data)

        wheatyield_card_html = generate_status_card("Total Wheat Yield", f"{total_wheat_yield:.2f}")
        st.markdown(wheatyield_card_html, unsafe_allow_html=True)
    with col6:
        total_kharifsorghum_yield = get_kharifsorghum_yield(selected_state, selected_district, selected_years, data)

        kharifsorghum_card_html = generate_status_card("Total Kharif Sorghum Yield", f"{total_kharifsorghum_yield:.2f}")
        st.markdown(kharifsorghum_card_html, unsafe_allow_html=True)
    with col7: 
        total_rabisorghum_yield = get_rabisorghum_yield(selected_state, selected_district, selected_years, data)

        rabisorghum_card_html = generate_status_card("Total Rabi Sorghum Yield", f"{total_rabisorghum_yield:.2f}")
        st.markdown(rabisorghum_card_html, unsafe_allow_html=True)
        
    col8,col9=st.columns([2,2])
    with col8:
        # Create a filled area chart for rice yield and rice production
        filtered_data = data[
            (data['State Name'] == selected_state) &
            (data['Dist Name'] == selected_district) &
            ((data['Year'] >= selected_years[0]) & (data['Year'] <= selected_years[1]))
        ]

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=filtered_data['Year'], y=filtered_data['RICE YIELD (Kg per ha)'],
                                 mode='lines', name='Rice Yield'))

        fig.add_trace(go.Scatter(x=filtered_data['Year'], y=filtered_data['RICE PRODUCTION (1000 tons)'],
                                 mode='lines', name='Rice Production'))

        fig.update_layout(title='Rice Yield vs Production Over Time',
                          xaxis_title='Year',
                          yaxis_title='Amount',
                          showlegend=True)

        # Apply fill attribute to each trace individually and set line color
        fig.update_traces(fill='tozeroy', selector=dict(type='scatter'), line=dict(color='#008000'))

        st.plotly_chart(fig, use_container_width=True)
    
    with col9:
        # Create a filled area chart for wheat yield and wheat production
        filtered_data = data[
            (data['State Name'] == selected_state) &
            (data['Dist Name'] == selected_district) &
            ((data['Year'] >= selected_years[0]) & (data['Year'] <= selected_years[1]))
        ]

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=filtered_data['Year'], y=filtered_data['WHEAT YIELD (Kg per ha)'],
                                 mode='lines', name='Wheat Yield'))

        fig.add_trace(go.Scatter(x=filtered_data['Year'], y=filtered_data['WHEAT PRODUCTION (1000 tons)'],
                                 mode='lines', name='Wheat Production'))

        fig.update_layout(title='Wheat Yield vs Production Over Time',
                          xaxis_title='Year',
                          yaxis_title='Amount',
                          showlegend=True)

        # Apply fill attribute to each trace individually and set line color
        fig.update_traces(fill='tozeroy', selector=dict(type='scatter'), line=dict(color='#008000'))

        st.plotly_chart(fig, use_container_width=True)
    col10,col11=st.columns([2,2])
    with col10:
            #st.subheader("Rice and Wheat Yield Stacked Bar Chart")

       

            stacked_bar_chart = get_stacked_bar_chart(selected_state, selected_district, selected_years, data)

            st.plotly_chart(stacked_bar_chart, use_container_width=True)
            
    with col11:
        crop_donut_chart = generate_crop_donut_chart(selected_state, selected_district, selected_years,data)
        st.plotly_chart(crop_donut_chart, use_container_width=True)
   
    col12,col13=st.columns([2,2])
    with col12:
        crop_names = ['SAFFLOWER', 'RAPESEED AND MUSTARD', 'CASTOR', 'LINSEED']
        crop_yield_line_chart = get_crop_yield_line(selected_state, selected_district, selected_years, data, crop_names)
        st.plotly_chart(crop_yield_line_chart, use_container_width=True)
        
    with col13:
        kharif_rabi_sorghum_yield_chart = get_kharif_rabi_sorghum_yield(selected_state, selected_district, selected_years, data)

# Display the chart
        st.plotly_chart(kharif_rabi_sorghum_yield_chart, use_container_width=True)
        
if __name__ == "__main__":
    app()