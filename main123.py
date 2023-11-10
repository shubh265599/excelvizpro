import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import plotly.graph_objects as go

st.set_page_config(
    page_title='ExcelViz Pro',
    page_icon='✅',
    layout='wide'
)

# Upload the background image
background_image = 'excelvizprocopy.jpg'

# Set the background image with transparency
st.write(f'''
    <style>
        .background-container {{
            background-image: url("data:image/jpg;base64,{base64.b64encode(open(background_image, "rb").read()).decode()}") !important;
            background-size: cover;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            opacity: 0.7; /* Adjust the opacity value as needed */
        }}
        .stApp {{
            background-color: rgba(255, 255, 255, 0.9); /* Adjust the last value (0.9) for the content area transparency */
        }}
    </style>
''', unsafe_allow_html=True)

# Create a container for the background image
st.markdown('<div class="background-container"></div>', unsafe_allow_html=True)

# Display the logo image
#st.image("excelvizpro.png", use_column_width=True, caption="ExcelViz Pro Logo")


def generate_html_download_link(fig):
    fig.write_html("plot.html", include_plotlyjs="cdn")
    with open("plot.html", "rb") as file:
        html = file.read()
        b64 = base64.b64encode(html).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="plot.html">Download Plot</a>'
        return st.markdown(href, unsafe_allow_html=True)

st.title('ExcelViz Pro 📈')
st.subheader('Upload an Excel file for analysis and visualization')

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

uploaded_file = st.file_uploader('Choose a file', type=['xlsx', 'csv'])

if uploaded_file:
    st.markdown('---')
    st.subheader('Data Analysis and Visualization:')

    try:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        elif uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload an XLSX or CSV file.")
            st.stop()

        if df.empty:
            st.error("The uploaded file is empty.")
            st.stop()

        st.dataframe(df)

        selected_columns = st.multiselect("Select columns for visualization", df.columns)
        if not selected_columns:
            st.warning("Please select at least one column for visualization.")
        else:
            chart_type = st.selectbox("Select a chart type", ["Line Chart", "Bar Chart", "Pie Chart", "Map"])

            if chart_type == "Line Chart":
                st.subheader("Line Chart:")
                for column in selected_columns:
                    if df[column].dtype in ['int64', 'float64']:
                        fig = px.line(df, x=df.index, y=column, title=f'{column} Line Chart')
                        st.plotly_chart(fig)

            elif chart_type == "Bar Chart":
                st.subheader("Bar Chart:")
                x_column = st.selectbox("Select X-Axis Column", selected_columns)
                y_column = st.selectbox("Select Y-Axis Column", selected_columns)
                fig = px.bar(df, x=x_column, y=y_column, title=f'Bar Chart: {x_column} vs. {y_column}')
                st.plotly_chart(fig)

            elif chart_type == "Pie Chart":
                st.subheader("Pie Chart:")
                values_column = st.selectbox("Select Values Column", selected_columns)
                labels_column = st.selectbox("Select Labels Column", selected_columns)
                fig = px.pie(df, values=values_column, names=labels_column, title=f'Pie Chart: {values_column} by {labels_column}')
                st.plotly_chart(fig)
                
            elif chart_type == "Map":
                st.subheader("Map:")
                latitude_column = st.selectbox("Select Latitude Column", df.columns)
                longitude_column = st.selectbox("Select Longitude Column", df.columns)
                fig = go.Figure(go.Scattermapbox(
                    lat=df[latitude_column],
                    lon=df[longitude_column],
                    mode='markers',
                    marker=go.scattermapbox.Marker(
                        size=9,
                        opacity=0.6,
                    ),
                    text=df.index,
                ))
                fig.update_layout(
                    hovermode='closest',
                    mapbox=go.layout.Mapbox(
                        style="open-street-map",
                        center=go.layout.mapbox.Center(
                            lat=df[latitude_column].mean(),
                            lon=df[longitude_column].mean(),
                        ),
                        zoom=10,
                    ),
                )
                st.plotly_chart(fig)
                
            st.subheader('Downloads:')
            generate_html_download_link(fig)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
