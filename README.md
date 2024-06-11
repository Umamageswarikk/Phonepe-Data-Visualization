 Problem Statement:
 
 The Phonepepulse Github repository contains a large amount of data related to
 various metrics and statistics.Th egoal is to extract this data and process it to obtain
 insights and information that can be visualized in a user-friendly manner.
 
 The solution must include the following steps:
 1. Extract data from the Phonepepulse Github repository through scripting and
 clone it..
 2. Transform the data into a suitable format and perform any necessary cleaning
 and pre-processing steps.
 3. Insert the transformed data into a MySQL database for efficient storage and
 retrieval.
 4. Create a live geovisualization dashboard using Streamlit and Plotly in Python
 to display the data in an interactive and visually appealing manner.
 5. Fetch the data from the MySQL database to display in the dashboard.
 6. Provideat least 10 different dropdown options for users toselectdifferent
 facts and figures to display on the dashboard

Approach:

Data Extraction:

Clone the GitHub repository using scripting to fetch the data from the PhonePe Pulse GitHub repository.
Store the data in a suitable format such as CSV or JSON.

Data Transformation:

Use a scripting language such as Python, along with libraries such as Pandas, to manipulate and pre-process the data.
This may include cleaning the data, handling missing values, and transforming the data into a format suitable for analysis and visualization.

Database Insertion:

Use the mysql-connector-python library in Python to connect to a MySQL database.
Insert the transformed data into the database using SQL commands.

Dashboard Creation:

Use the Streamlit and Plotly libraries in Python to create an interactive and visually appealing dashboard.
Plotly's built-in geo map functions can be used to display the data on a map.
Streamlit can be used to create a user-friendly interface with multiple dropdown options for users to select different facts and figures to display.

Data Retrieval:

Use the mysql-connector-python library to connect to the MySQL database and fetch the data into a Pandas DataFrame.
Use the data in the DataFrame to update the dashboard dynamically.

Deployment:

Ensure the solution is secure, efficient, and user-friendly.
Test the solution thoroughly.
Deploy the dashboard publicly, making it accessible to users.
