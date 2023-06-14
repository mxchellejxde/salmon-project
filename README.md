# Exploration of the Salmon Population Through the Years:

## Description
The aim of our project is to explore and visualize the trends and factors impacting the salmon population on the West Coast. We aim to investigate relationships between population changes over time, locations with higher or lower population densities, and other related correlations that may emerge from the data.

For this project, we were required to create visualizations with a Python Flask-powered API, HTML/CSS, JavaScript, and at least one database (SQL, MongoDB, SQLite, etc.). User-driven interaction will be a key feature of our visualization, with interactive elements such as dropdowns to select a specific species or year, and textboxes for searching specific locations. Our final visualization will ideally present at least three different views of the data, such as temporal trends, geographical distribution, and environmental correlations.

We will ensure the data story is clear, visually appealing, and easy to understand for users of all levels. The final page will be designed to run without errors, providing a seamless experience for the end user.

## Installation/Programs
- Javascript
- Python
  - Import `Flask, jsonify, render_template` from `Flask`
  - Import `CORS` from `flask_cors`
  - Import `MongoClient, errors` from `pymongo`
  - Import `json`  
  - Import `logging`
- HTML

## Data Sources
1. [The National Oceanic and Atmospheric Administration (NOAA) Fisheries Data](https://www.webapps.nwfsc.noaa.gov/apex/parrdata/inventory/tables/table/population_data_and_references_for_the_salmon_population_summary_sps_database): They maintain extensive data sets on fisheries, including salmon population numbers.
2. [Flask GeoAPI](https://gis-ops.com/flask-geo-api-tutorial-powerful-geospatial-flask-explained/): Collection of the map coordinates

## Data Visualizations
1. A US map that includes the 5 different types of salmon species and their geographic locations. Each species is differentiated by different color bubbles, and the size of the bubbles represent the total number of salmon that inhabit a specific coordinate.
2. A bar graph that represents each salmon species' number of spawners over the years. Selecting the species in the dropdown will update the graph to reflect the selected salmon's spawners.
3. A line graph that includes the 5 different types of salmon species and the number of spawners over the years
4. A map that shows the locations of the total hatchery salmon and wild salmon populations
5. A line chart:
   - There are five line charts, one for each species: Chinook, Chum, Coho, Sockeye, and Steelhead.
   - Each line chart represents the trend of three variables over different brood years: Wild Salmon Total, Hatchery Salmon      Total, and Number Of Spawners.
   - The line chart uses the Chart.js library to visualize the data.
   - The data for each line chart is retrieved from the Flask application's endpoints /line/data/<species>.
   - The line chart is drawn using the HTML canvas element with an ID based on the species name (myChart<Species>).
 6. A doughnut chart:
    - There are five doughnut charts, one for each species: Chinook, Chum, Coho, Sockeye, and Steelhead.
    - Each doughnut chart represents the population distribution of Wild Salmon and Hatchery Salmon for specific brood     -       years.
    - The doughnut chart uses the Chart.js library to visualize the data.
    - The data for each doughnut chart is retrieved from the Flask application's endpoints /doughnut/data/<species>.
    - The doughnut chart is drawn using the HTML canvas element with an ID based on the species name (<species>Chart).

## Process
1. *Data Gathering*: 
   - Access the data sources and extract into CSV files
   - Clean the data of missing values and unnecessary information
2. *Backend Development*:
   - Combining the dataset into a unified dataset
   - Select a database, `MongoDB`, to set up and store our dataset
   - Create a `Python Flask API` for interacting with our database
   - Develop API endpoints for retrieving and manipulating the data
3. *Frontend Development*:
   - Create the `HTML/CSS` layout for the dashboard
   - Implement `JavaScript` for frontend interactivity and data visualization
4. *Data Visualization*:
   - Design and implement a time series visualization to display population trends over time
   - Create a geographic distribution visualization using Leaflet
   - Develop additional visualizations to display environmental factors impacting salmon populations
5. *User Interaction*:
   - Implement interactive elements such as dropdowns, text boxes, and filters
   - Ensure all interactive elements are functioning correctly and updating the visualizations as expected

## Credits
- [MJ](https://github.com/mxchellejxde)
- [Nicole](https://github.com/Nicolemarie717) 
- [Eli](https://github.com/elitracewell)
- [Michael](https://github.com/dibartm)
