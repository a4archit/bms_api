"""
BMS-API
======

        I work on this project to make my skills more strong.
"""




# Dependencies
from fastapi import FastAPI, Path, Query, HTTPException
from typing import List
import json 




# loading data
def load_data() -> dict :
    """ this function will return the json dataset """
    with open('books_data.json', 'r') as file:
        data = json.load(file)

    return data





# creating instance of FastAPI class and loading data
app = FastAPI()
DATA = load_data()
valid_data_keys = list(list(DATA.values())[0].keys()) # extracting data keys of first instance
valid_data_keys.insert(0, 'all')









# ====================================== Creating Routes ========================== #




# general route (/)
@app.get("/")
def general_routes():
    """ this function will display the basic information of the routes """

    routes_basic_info: dict = {
        "/": "Display the basic informations to the another routes",
        "/data": "Display the whole data",
        "/XXXXXXXXXXXXX": "13-digits ISBN ID",
        "/search": "Display the data of searched result (see original docs for this)"
    }

    return routes_basic_info






# route (/data) for whole data
@app.get("/data")
def whole_data():
    """ this function will display the whole data """
    return DATA






# route (/XXXXXXXXXXXXX) ISBN for returning data of particular instance
@app.get("/{isbn}")
def particular_book_data(
    isbn: str = Path(..., title="ISBN of particular Book", example="9780002005883", description="This is the ISBN ID of particular Book, it's digits length should be of 10 or 13."),
    key: str = Query('all', title="Any key for particular value", examples=valid_data_keys, description=f"You can get the exact value of any field (what you want), valid keys are {valid_data_keys}")
    ) -> dict :
    
    """ this function will return the data of particular book (according to the provided isbn id) """
    if isbn not in DATA:
        raise HTTPException(status_code=400, detail=f"Invalid ISBN number {isbn}, please enter valid number.")

    if key not in valid_data_keys:
        raise HTTPException(status_code=400, detail=f"Inavlid key '{key}', valid keys are {valid_data_keys}")
    
    

    data_fetched: dict = DATA[isbn]

    if key != 'all':
        return {key: data_fetched[key]}
    
    return data_fetched










if __name__ == "__main__":

    print("starting data loading.... ", end = " ")
    data = load_data()
    print("data loaded successfully")
    print(type(data))




