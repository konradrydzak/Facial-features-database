# Facial features database

Simple web app for user testing a database filtering functionality with facial feature attributes and an images database (created for master thesis purposes).

You can preview the app at: [share.streamlit.io](https://share.streamlit.io/konradrydzak/facial-features-database/facial_features_database.py)

## Setup

1. Fill in required detail about *MONGODB_EXTERNAL_PORT* in *.env* file:
2. Run command: `docker-compose up -d`
3. Use created mongodb instance *URI* in *database.ini* file (example: *URI=mongodb://localhost:<MONGODB_EXTERNAL_PORT>*)
4. Run program with command: `streamlit run facial_features_database.py`
5. Web app should be running at: http://localhost:8501/

## Skills used

- using NoSQL MongoDB database (with both: local instances and cloud database on MongoDB Atlas service)
- using PyMongo distribution for connecting and querying data from database
- hosted images on AWS (courtesy of a friend Wiktor *~ thanks!*)
- provided both original and cropped images 
- prepared an option to filter database based both: on attributes originally from initial database and attributes predicted by a deep neural network (created for master thesis purposes)

### Possible improvements

- user UI and quality of life improvements (*mostly depends on future streamlit features and updates*)
- *"cheat"* code fragments cleanup - it results from streamlit limitation, maybe possible to fulfill in the future...