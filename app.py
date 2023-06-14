import logging
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient, errors
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb+srv://Eli:Ourgrouprocks123@salmonpopulation.samyjbo.mongodb.net/SalmonPopulation"

mongo = PyMongo(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_stream_coordinates(collection):
    stream_coordinates = {}
    cursor = collection.find()
    for doc in cursor:
        stream_name = doc.get('Stream Name')  # Replace 'stream_name_field' with the actual field name
        latitude = float(doc.get('Latitude'))
        longitude = float(doc.get('Longitude'))
        if stream_name:
            stream_coordinates[stream_name] = {'Latitude': latitude, 'Longitude': longitude}
    return stream_coordinates

@app.route('/salmonData')
def get_salmon_data():
    username = "Eli"
    password = "Ourgrouprocks123"
    cluster = "salmonpopulation.samyjbo.mongodb.net"
    client = MongoClient(f"mongodb+srv://{username}:{password}@{cluster}/")
    
    try:
        client.server_info()
        print("Connected to MongoDB Server")
    except errors.ServerSelectionTimeoutError as err:
        print("Could not connect to MongoDB Server:", err)
        return "Could not connect to MongoDB Server", 500

    db = client['SalmonPopulation']
    salmon_data = db['salmon_coordinates_weather_df']
    salmon_doc = salmon_data.find()
    salmon_info = {}
    table = []
    for doc in salmon_doc:
        doc.pop('_id', None)
        table.append(doc)

    return jsonify(table)

@app.route('/data', methods=['GET'])
def get_data():
    username = "SalmonPopulation"
    password = "Welcome123"
    cluster = "salmonpopulation.samyjbo.mongodb.net"
    client = MongoClient(f"mongodb+srv://{username}:{password}@{cluster}/")

    try:
        client.server_info()
        logger.info("Connected to MongoDB Server")
    except errors.ServerSelectionTimeoutError as err:
        logger.error("Could not connect to MongoDB Server: %s", err)
        return "Could not connect to MongoDB Server", 500

    db = client['SalmonPopulation']
    species_tables = ['Chinook_map_table', 'Chum_map_table', 'Coho_map_table', 'Sockeye_map_table', 'Steelhead_map_table']

    stream_coordinates_collection = db['stream_coordinates']
    stream_coordinates = get_stream_coordinates(stream_coordinates_collection)

    output = {}

    for table in species_tables:
        collection = db[table]
        documents = collection.find()
        table_data = []
        total_documents = collection.count_documents({})
        processed_documents = 0

        for doc in documents:
            doc.pop('_id', None)
            stream_name = doc['Stream Name']
            if stream_name in stream_coordinates:
                doc.update(stream_coordinates[stream_name])

            hatchery_total = doc.get('Hatchery Salmon Total', 0)
            wild_total = doc.get('Wild Salmon Total', 0)
            doc['Total Population'] = hatchery_total + wild_total
            table_data.append(doc)
            processed_documents += 1
            logger.info(f"Processed {processed_documents}/{total_documents} documents in table {table}")

        output[table] = table_data

    return jsonify(output)

@app.route('/chart', methods=['GET'])
def get_chart():
    return render_template('chart.html')

@app.route('/chart-data/<int:year>', methods=['GET'])
def get_chart_data_for_year(year):
    output = get_data()
    if isinstance(output, str):  # Check if get_data() returned an error string
        return jsonify({'error': output}), 500
    output = output.json
    species_populations = {}
    for table, data in output.items():
        species = table.split('_')[0]  # Extract species name from the table name
        data_for_year = [item for item in data if item['Brood Year'] == year]
        hatchery_population = sum(item['Hatchery Salmon Total'] for item in data_for_year)
        wild_population = sum(item['Wild Salmon Total'] for item in data_for_year)
        species_populations[species] = {'hatchery': hatchery_population, 'wild': wild_population}
    return jsonify(species_populations)

def get_line_data_for_species(species, year=None):  
    pipeline = [
        {"$match": {"Brood Year": {"$gte": 1980}}},
        {"$group": {
            "_id": "$Brood Year",
            "Wild Salmon Total": {"$sum": "$Wild Salmon Total"},
            "Hatchery Salmon Total": {"$sum": "$Hatchery Salmon Total"},
            "Number Of Spawners": {"$sum": "$Number Of Spawners"},
        }},
        {"$sort": {"_id": 1}}
    ]

    if year:
        pipeline.insert(1, {"$match": {"Brood Year": year}})

    data = mongo.db[f"{species.capitalize()}_map_table"].aggregate(pipeline)
    data_list = [{"Brood Year": item["_id"],
                  "Wild Salmon Total": item["Wild Salmon Total"],
                  "Hatchery Salmon Total": item["Hatchery Salmon Total"],
                  "Number Of Spawners": item["Number Of Spawners"]}
                 for item in data]
    return jsonify(data_list)

@app.route('/line/data/<species>', methods=['GET'])
def get_line_species_data(species):
    year = request.args.get('year')  # Get the year from query parameter
    return get_line_data_for_species(species, year)

def get_doughnut_data_for_species(species):  
    pipeline = [
        {"$match": {"Brood Year": {"$in": [1985, 1990, 1995, 2000, 2005, 2010]}}},
        {"$group": {
            "_id": "$Brood Year",
            "Wild Salmon Total": {"$sum": "$Wild Salmon Total"},
            "Hatchery Salmon Total": {"$sum": "$Hatchery Salmon Total"},
            "Number Of Spawners": {"$sum": "$Number Of Spawners"},
        }},
        {"$sort": {"_id": 1}}
    ]
    data = mongo.db[f"{species.capitalize()}_map_table"].aggregate(pipeline)
    data_list = [{"Brood Year": item["_id"],
                  "Wild Salmon Total": item["Wild Salmon Total"],
                  "Hatchery Salmon Total": item["Hatchery Salmon Total"],
                  "Number Of Spawners": item["Number Of Spawners"]}
                 for item in data]
    return jsonify({
        "species": species,
        "brood_years": [1985, 1990, 1995, 2000, 2005, 2010],
        "data": data_list
    })

@app.route('/doughnut/data/<species>', methods=['GET'])
def get_doughnut_species_data(species):
    return get_doughnut_data_for_species(species)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/PopTotal')
def pop_total():
    return render_template('PopTotal.html')

@app.route('/map', methods=['GET'])
def get_map():
    return render_template('map.html')

if __name__ == "__main__":
    app.run(debug=True)
