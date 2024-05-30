import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
from datetime import datetime
from PIL import Image

# Set wide screen mode
st.set_page_config(layout="wide")

# Title and Introduction
st.title('Mastering Streamlit: A Comprehensive Professional Guide')

st.markdown("""
This tutorial is designed to help you master Streamlit by exploring advanced functionalities and features. 
You'll learn how to use Streamlit effectively to build interactive and professional web applications.
""")

# Sidebar for navigation
st.sidebar.header("Tutorial Sections")
sections = [
    "Introduction", "Basic Widgets", "Advanced Widgets", "Layouts and Styling", "Caching", 
    "Interactive Visualizations", "API Integration", "Session State", "Theming", "User Authentication", 
    "Custom Components", "Data Manipulation", "Forms Handling", "Advanced Theming", "Deploying Streamlit Apps", 
    "File Uploads", "Working with Media", "Matplotlib Charts", "Seaborn Charts", "Altair Charts", "Custom Widgets",
    "Multi-page Navigation", "Streamlit and Docker", "Machine Learning Workflows", "Connecting to Databases", 
    "Real-time Data Updates"
]
choice = st.sidebar.selectbox("Select a section:", sections)

# Introduction to Streamlit
if choice == "Introduction":
    st.header("Introduction to Streamlit")
    st.markdown("""
    Streamlit is an open-source app framework for creating and sharing beautiful, custom web apps for machine learning and data science. 
    In just a few minutes you can build and deploy powerful data apps.
    """)

# Basic Widgets
elif choice == "Basic Widgets":
    st.header("Basic Widgets")
    st.markdown("Explore basic Streamlit widgets to make your applications interactive.")

    st.subheader("Text Input")
    user_name = st.text_input("Enter your name:")
    if user_name:
        st.write(f'Hello, {user_name}!')

    st.subheader("Slider")
    age = st.slider("Select your age:", 0, 100, 25)
    st.write(f'Your age: {age}')

    st.subheader("Checkbox")
    if st.checkbox('Show greeting'):
        st.write("Hello, Streamlit user!")

# Advanced Widgets
elif choice == "Advanced Widgets":
    st.header("Advanced Widgets")
    st.markdown("Learn about advanced widgets for more complex interactions.")

    st.subheader("File Uploader")
    uploaded_file = st.file_uploader("Choose a CSV file")
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)

    st.subheader("Multiselect")
    options = st.multiselect(
        'Select your favorite fruits',
        ['Apple', 'Banana', 'Orange', 'Grapes', 'Mango'],
        ['Apple', 'Mango']
    )
    st.write('You selected:', options)

# Layouts and Styling
elif choice == "Layouts and Styling":
    st.header("Layouts and Styling")
    st.markdown("Organize your app's layout using columns and expanders, and style your app with themes.")

    st.subheader("Columns")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Column 1")
        st.write("Content for column 1")
    with col2:
        st.header("Column 2")
        st.write("Content for column 2")
    with col3:
        st.header("Column 3")
        st.write("Content for column 3")

    st.subheader("Expander")
    with st.expander("Expand to see more"):
        st.write("Hidden content!")

# Caching with Decorators
elif choice == "Caching":
    st.header("Caching with Decorators")
    st.markdown("""
    Use Streamlit's caching to speed up your app by storing the results of expensive computations.
    The `@st.cache_data` decorator is used to cache data-loading functions.
    """)

    @st.cache_data
    def load_data(nrows):
        data = pd.DataFrame({
            'numbers': np.random.rand(nrows),
            'letters': np.random.choice(['a', 'b', 'c'], nrows)
        })
        return data

    st.subheader("Load Data with Caching")
    if st.button('Load Data'):
        data = load_data(1000)
        st.write(data)

    st.markdown("""
    The `@st.cache_data` decorator caches the result of the function, so subsequent calls with the same arguments will be much faster.
    """)

# Interactive Visualizations
elif choice == "Interactive Visualizations":
    st.header("Interactive Visualizations with Plotly")
    st.markdown("""
    Use Plotly for dynamic and interactive visualizations.
    """)

    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Berries", "Melons"],
        "Amount": [20, 35, 30, 10, 15],
        "City": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
    })
    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# API Integration
elif choice == "API Integration":
    st.header("API Integration")
    st.markdown("""
    Integrate external APIs to enhance your app's functionality.
    """)

    api_input = st.text_input("Enter your query to fetch data (e.g., 'Streamlit'):")
    api_button = st.button("Fetch from API")
    if api_button:
        api_response = requests.get(f"https://api.publicapis.org/entries?title={api_input}")
        apis = api_response.json()
        st.write("API response:", apis)

# Session State
elif choice == "Session State":
    st.header("Session State Management")
    st.markdown("""
    Manage state across sessions to create interactive apps where user inputs and actions persist over multiple interactions.
    The `@st.cache_data` and `@st.cache_resource` decorators are also used to cache resources.
    """)

    @st.cache_resource
    def get_counter():
        return 0

    if 'counter' not in st.session_state:
        st.session_state.counter = get_counter()

    increment = st.button("Increment")
    if increment:
        st.session_state.counter += 1
    st.write("Current count:", st.session_state.counter)

    st.markdown("""
    The `@st.cache_resource` decorator is used to cache objects that you might want to share across your app, like a database connection.
    """)

# Theming
elif choice == "Theming":
    st.header("Theming")
    st.markdown("""
    Customize your Streamlit app's appearance using theming.
    """)

    st.markdown("""
    You can configure the theme in your Streamlit configuration file (`.streamlit/config.toml`):
    ```toml
    [theme]
    primaryColor = "#F63366"
    backgroundColor = "#FFFFFF"
    secondaryBackgroundColor = "#F0F2F6"
    textColor = "#262730"
    font = "sans serif"
    ```
    """)

# User Authentication
elif choice == "User Authentication":
    st.header("User Authentication")
    st.markdown("""
    Implement user authentication to secure your app.
    """)

    st.markdown("**This is a placeholder for integrating user authentication.**")

# Custom Components
elif choice == "Custom Components":
    st.header("Custom Components")
    st.markdown("""
    Create custom components using frontend technologies like React for tailored functionalities.
    """)

    st.markdown("**This is a placeholder for integrating custom React components.**")

# Data Manipulation
elif choice == "Data Manipulation":
    st.header("Data Manipulation")
    st.markdown("""
    Manipulate and transform data directly within Streamlit.
    """)

    # Sample DataFrame
    st.subheader("Sample DataFrame")
    df = pd.DataFrame({
        "Name": ["John", "Jane", "Mary", "Peter"],
        "Age": [28, 34, 29, 42],
        "City": ["New York", "Los Angeles", "Chicago", "Houston"]
    })
    st.write(df)

    # Data Transformation
    st.subheader("Data Transformation")
    df["Age in 10 years"] = df["Age"] + 10
    st.write(df)

# Forms Handling
elif choice == "Forms Handling":
    st.header("Forms Handling")
    st.markdown("""
    Use forms to handle multiple input elements and control the submission process.
    """)

    st.subheader("Form Example")
    with st.form(key='my_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        st.write(f"Username: {username}, Password: {password}")

# Advanced Theming
elif choice == "Advanced Theming":
    st.header("Advanced Theming")
    st.markdown("""
    Further customize your app with advanced theming options.
    """)

    st.markdown("""
    In addition to the basic theming, you can use custom CSS to style your Streamlit app. 
    Here is an example of adding a custom CSS file to your Streamlit app:
    ```python
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    local_css("style.css")
    ```
    """)

# Deploying Streamlit Apps
elif choice == "Deploying Streamlit Apps":
    st.header("Deploying Streamlit Apps")
    st.markdown("""
    Learn how to deploy your Streamlit apps using Streamlit Sharing, Heroku, or other cloud platforms.
    """)

    st.subheader("Streamlit Sharing")
    st.markdown("""
    Streamlit Sharing is the easiest way to deploy Streamlit apps. Just push your app to a public GitHub repo and deploy it with Streamlit Sharing.
    1. Put your app in a public GitHub repo (and make sure it has a requirements.txt!)
    2. Sign in to share.streamlit.io
    3. Click 'Deploy an app' and then paste in your GitHub URL
    """)

    st.subheader("Deploying on Heroku")
    st.markdown("""
    You can also deploy your Streamlit app on Heroku. Here's a basic guide:
    1. Create a `Procfile` in your repo with the following content: `web: streamlit run your_script.py`
    2. Create a `requirements.txt` with all the dependencies.
    3. Install the Heroku CLI and run the following commands:
    ```bash
    heroku create
    git push heroku master
    heroku open
    ```
    """)

# File Uploads
elif choice == "File Uploads":
    st.header("Handling File Uploads")
    st.markdown("""
    Streamlit supports file uploads, which can be processed in various ways.
    """)

    st.subheader("Upload CSV or Excel File")
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            data = pd.read_excel(uploaded_file)
        st.write(data)

# Working with Media
elif choice == "Working with Media":
    st.header("Working with Media")
    st.markdown("""
    Streamlit allows you to display images, audio, and videos.
    """)

    st.subheader("Display an Image")
    image = Image.open('sample_image.jpg')
    st.image(image, caption='Sample Image', use_column_width=True)

    st.subheader("Play a Video")
    video_file = open('sample_video.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

    st.subheader("Play an Audio")
    audio_file = open('sample_audio.mp3', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes)

# Matplotlib Charts
elif choice == "Matplotlib Charts":
    st.header("Matplotlib Charts")
    st.markdown("""
    You can integrate Matplotlib charts in your Streamlit app.
    """)

    st.subheader("Simple Line Plot")
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
    st.pyplot(fig)

# Seaborn Charts
elif choice == "Seaborn Charts":
    st.header("Seaborn Charts")
    st.markdown("""
    Seaborn is a Python visualization library based on Matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics.
    """)

    st.subheader("Seaborn Heatmap")
    data = np.random.rand(10, 12)
    fig, ax = plt.subplots()
    sns.heatmap(data, ax=ax)
    st.pyplot(fig)

# Altair Charts
elif choice == "Altair Charts":
    st.header("Altair Charts")
    st.markdown("""
    Altair is a declarative statistical visualization library for Python, based on Vega and Vega-Lite visualization grammars.
    """)

    st.subheader("Altair Scatter Plot")
    df = pd.DataFrame(np.random.randn(200, 3), columns=['a', 'b', 'c'])
    c = alt.Chart(df).mark_circle().encode(
        x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c']
    )
    st.altair_chart(c, use_container_width=True)

# Custom Widgets
elif choice == "Custom Widgets":
    st.header("Custom Widgets")
    st.markdown("""
    Create custom widgets using Streamlit components or frontend technologies like React.
    """)

    st.markdown("**This is a placeholder for integrating custom widgets.**")

# Multi-page Navigation
elif choice == "Multi-page Navigation":
    st.header("Multi-page Navigation")
    st.markdown("""
    Streamlit now supports multi-page applications, allowing developers to build larger and more complex apps with multiple separate pages.
    """)

    st.markdown("**This is a placeholder for demonstrating multi-page navigation.**")

# Streamlit and Docker
elif choice == "Streamlit and Docker":
    st.header("Streamlit and Docker")
    st.markdown("""
    Deploy your Streamlit app using Docker for consistent and scalable deployment.
    """)

    st.subheader("Dockerfile Example")
    st.markdown("""
    Here's an example of a Dockerfile to containerize your Streamlit app:
    ```Dockerfile
    # Use the official Python image from the Docker Hub
    FROM python:3.9

    # Set the working directory in the container
    WORKDIR /app

    # Copy the current directory contents into the container at /app
    COPY . /app

    # Install any needed packages specified in requirements.txt
    RUN pip install --no-cache-dir -r requirements.txt

    # Make port 8501 available to the world outside this container
    EXPOSE 8501

    # Run streamlit when the container launches
    CMD ["streamlit", "run", "your_script.py"]
    ```
    """)
    st.subheader("Building and Running the Docker Container")
    st.markdown("""
    To build and run the Docker container, use the following commands:
    ```bash
    # Build the Docker image
    docker build -t streamlit-app .

    # Run the Docker container
    docker run -p 8501:8501 streamlit-app
    ```
    """)

# Machine Learning Workflows
elif choice == "Machine Learning Workflows":
    st.header("Machine Learning Workflows")
    st.markdown("""
    Integrate machine learning models into your Streamlit app for interactive data analysis and prediction.
    """)

    from sklearn.datasets import load_iris
    from sklearn.ensemble import RandomForestClassifier

    st.subheader("Iris Dataset Example")
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['species'] = iris.target
    st.write(df.head())

    st.subheader("Train a Random Forest Classifier")
    model = RandomForestClassifier()
    model.fit(iris.data, iris.target)
    st.write("Model trained successfully!")

    st.subheader("Make Predictions")
    sepal_length = st.slider("Sepal Length", float(df['sepal length (cm)'].min()), float(df['sepal length (cm)'].max()))
    sepal_width = st.slider("Sepal Width", float(df['sepal width (cm)'].min()), float(df['sepal width (cm)'].max()))
    petal_length = st.slider("Petal Length", float(df['petal length (cm)'].min()), float(df['petal length (cm)'].max()))
    petal_width = st.slider("Petal Width", float(df['petal width (cm)'].min()), float(df['petal width (cm)'].max()))

    prediction = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])
    st.write("Predicted Species:", iris.target_names[prediction][0])

# Connecting to Databases
elif choice == "Connecting to Databases":
    st.header("Connecting to Databases")
    st.markdown("""
    Connect your Streamlit app to various databases to fetch and display data.
    """)

    st.subheader("Connecting to a SQLite Database")
    st.markdown("""
    Here's an example of how to connect to a SQLite database:
    ```python
    import sqlite3

    # Connect to SQLite database
    conn = sqlite3.connect('example.db')

    # Create a cursor object
    cur = conn.cursor()

    # Execute a query
    cur.execute("SELECT * FROM users")

    # Fetch the results
    rows = cur.fetchall()

    # Close the connection
    conn.close()
    ```

    Display the results:
    ```python
    st.write(rows)
    ```
    """)

# Real-time Data Updates
elif choice == "Real-time Data Updates":
    st.header("Real-time Data Updates")
    st.markdown("""
    Use Streamlit's ability to handle real-time data updates for dynamic applications.
    """)

    st.subheader("Real-time Chart Example")
    import time

    data = pd.DataFrame(np.random.randn(10, 2), columns=['a', 'b'])

    chart = st.line_chart(data)

    for i in range(100):
        new_data = pd.DataFrame(np.random.randn(10, 2), columns=['a', 'b'])
        chart.add_rows(new_data)
        time.sleep(0.1)

# Conclusion
st.markdown("---")
st.markdown("""
This comprehensive tutorial provided an in-depth look at Streamlit's advanced functionalities. 
By mastering these features, you can build dynamic, responsive, and sophisticated web applications.
""")
