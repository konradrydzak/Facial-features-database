from configparser import ConfigParser

import pymongo
import streamlit as st

# streamlit page setup

st.set_page_config(
    page_title="Facial features database",
    page_icon=":man:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# MongoDB connection setup


@st.cache_resource
def mongodb_connection_and_collection_setup():
    config_file = ConfigParser()
    config_file.read("database.ini")
    URI = config_file['MONGODB']['URI']

    try:
        client = pymongo.MongoClient(URI)
    except pymongo.errors.ConfigurationError:
        client = pymongo.MongoClient(st.secrets["URI"])
    db = client["facial_features_database"]

    return db["facial_features_collection"]


collection = mongodb_connection_and_collection_setup()

st.write('<style>div.stRadio > label {font-size:120%; font-weight:bold;}</style>', unsafe_allow_html=True)
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
st.write('<style>div.st-bf{flex-direction: column;} div.st-ag{padding-left:2px;}</style>', unsafe_allow_html=True)

# facial features names setup

features = ['5 o Clock Shadow', 'Arched Eyebrows', 'Attractive', 'Bags Under Eyes', 'Bald', 'Bangs', 'Big Lips',
            'Big Nose', 'Black Hair', 'Blond Hair', 'Blurry', 'Brown Hair', 'Bushy Eyebrows', 'Chubby',
            'Double Chin', 'Eyeglasses', 'Goatee', 'Gray Hair', 'Heavy Makeup', 'High Cheekbones', 'Male',
            'Mouth Slightly Open', 'Mustache', 'Narrow Eyes', 'No Beard', 'Oval Face', 'Pale Skin', 'Pointy Nose',
            'Receding Hairline', 'Rosy Cheeks', 'Sideburns', 'Smiling', 'Straight Hair', 'Wavy Hair',
            'Wearing Earrings', 'Wearing Hat', 'Wearing Lipstick', 'Wearing Necklace', 'Wearing Necktie', 'Young']

# page starts here

_, center, _ = st.columns([1, 1, 1])  # is used to "cheat" center alignment of elements
center.title(":blue[Facial features database]")

# mongodb request setup

original_or_predicted = st.radio(label="Filter database by: ",
                                 options=["Original dataset attributes", "Predicted attributes"], index=0,
                                 key="original_or_predicted")

nestedfield_dict = {}  # used in mongodb request query

for i in range(5):  # displays 40 facial features options in 5 rows and 8 columns each
    for index, col in enumerate(st.columns(8)):
        selected_option = col.radio(label=f"{features[index + i * 8]}: ", options=["Any", "True", "False"], index=0,
                                    key=features[index + i * 8])
        if selected_option == "True":
            nestedfield_dict[f"{features[index + i * 8]}"] = True
        elif selected_option == "False":
            nestedfield_dict[f"{features[index + i * 8]}"] = False

display_cropped = st.radio(label="Additionally display cropped images?", options=["Yes", "No"], index=1,
                           key="display_cropped")

if original_or_predicted == "Original dataset attributes":  # used in mongodb request query
    original_or_predicted = "original attributes"
else:
    original_or_predicted = "predicted attributes"

search = {f"{original_or_predicted}.{nestedfield_name}": nestedfield_value for nestedfield_name, nestedfield_value in
          nestedfield_dict.items()}

# streamlit session_state (state of the page on previous run) initiation

if 'displaying' not in st.session_state:  # parameter used to determine if user was using "Show previous/next page" buttons
    st.session_state.displaying = False
displaying = st.session_state.displaying

if 'start_index' not in st.session_state:
    st.session_state.start_index = 0
start_index = st.session_state.start_index


# additional function to skip clicking search if user was using "Show previous/next page" buttons

def is_displaying(next_batch, next_run_start_index, number_of_all_images, searched_results_list):
    st.session_state.displaying = True
    st.session_state.results_list = searched_results_list
    if next_batch:
        if next_run_start_index + 4 < number_of_all_images:
            next_run_start_index += 4
    else:
        next_run_start_index -= 4
        if next_run_start_index < 0:
            next_run_start_index = 0
    st.session_state.start_index = next_run_start_index


# Search function

search_clicked = st.button(label="Search")
if search_clicked or displaying:
    if len(search) <= 5:
        st.warning("It can take a while...")

    if 'results_list' not in st.session_state:
        st.session_state.results_list = list(collection.find(search))
    results_list = st.session_state.results_list

    number_of_images = len(results_list)
    st.success(f"Found: {number_of_images} images. ")

    end_index = start_index + 4
    if end_index > number_of_images:
        end_index = number_of_images

    if number_of_images != 0:
        st.header(f"Displaying {end_index - start_index} images (between indexes {start_index + 1} and {end_index}) out of {number_of_images}: ")
        col1, _, col2 = st.columns([1.5, 9.75, 1])
        col1.button(label="Show previous page", key="previous", on_click=is_displaying,
                    args=(False, start_index, number_of_images, results_list,))
        col2.button(label="Show next page", key="next", on_click=is_displaying,
                    args=(True, start_index, number_of_images, results_list,))
        if display_cropped == "Yes":
            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
            columns = [col1, col2, col3, col4, col5, col6, col7, col8]
            for i in range(start_index, end_index):
                columns[2 * (i - start_index)].image(image=results_list[i]["original image"],
                                                     caption=results_list[i]["filename"], width=200)
                columns[2 * (i - start_index) + 1].image(image=results_list[i]["cropped image"],
                                                         caption="Cropped image", width=178)
        else:
            col1, col2, col3, col4 = st.columns(4)
            columns = [col1, col2, col3, col4]
            for i in range(start_index, end_index):
                columns[i - start_index].image(image=results_list[i]["original image"],
                                               caption=results_list[i]["filename"], width=400)

    st.session_state.displaying = False  # resets three main session_state values if user does not use "Show previous/next page" buttons
    st.session_state.start_index = 0
    del st.session_state.results_list
