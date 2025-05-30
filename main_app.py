"""
BMS-API
======

        I work on this project to make my skills more strong.
"""




# Dependencies
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import Field, BaseModel, AnyUrl, EmailStr
from typing import List, Dict, Optional, Annotated
from datetime import datetime
import json 




# loading data
def load_data() -> dict :
    """ this function will return the json dataset """
    with open('books_data.json', 'r') as file:
        data = json.load(file)

    return data




# extracting current year
current_year = datetime.today().year



class Book(BaseModel):
    isbn13: Annotated[str, Field(..., title='ISBN', description='ISBN number of 13 digits', examples=['9780002005883'])]
    isbn10: Annotated[str, Field(title="ISBN 10", description="ISBN 10 is a unique number of 10 digits", examples=['0002005883'])]
    title: Annotated[str, Field(..., title='Title', description='Title of book (short text)')]
    subtitle: Annotated[Optional[int], Field(..., title='Subtitle', description='Subtitle of book')] = ""
    author: Annotated[str, Field(..., title='Author', description='Name of the book author.')]
    category: Annotated[Optional[str], Field(..., title='Category', description='Category of book')] = ""
    thumbnail: Annotated[AnyUrl, Field(..., title='Thumbnail URL', description='URL of book thumbnail')]
    description: Annotated[str, Field(..., title='Description', description='Description of the book')]
    published_year: Annotated[int, Field(gt=0, lt=current_year+1, title='Published year', description='Published year of the book')]
    average_rating: Annotated[Optional[float], Field(title='Average Rating', description='Average rating of book provide by users')] = None
    num_pages: Annotated[int, Field(..., title='Total pages', description='Total number of pages in the book')]
    ratings_count: Annotated[Optional[int], Field(..., title='Total Ratings', description='Total number of reviews given by the readers.')] = None






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





# route (/search) for searching an book across data
@app.get("/search/{query}")
def search(
        query: str = Path(..., title="Query that enter by user for searching", examples=['A walk to life (by title)', 'Aman Shrivaastava (by author)'], description="This is the search term (search query) that to be searched accross dataset."),
        search_key: str = Query('title', title="Search key for searching", examples=['title','author','year','isbn'], description="A search key tell server that hat exact will it search for given query."),
        items: int = Query(10, title="Total number of items to be returned", examples=[10, 20, 50], description="This is the total number of items that would be return after search the particular book.")
    ) -> dict :

    """  
        This function returns searched books data with respect to the search 
        key [title, author, etc] of number of elements [10, 20, 50, etc]
    """


    # defining some variables
    valid_search_keys = ['title', 'author','description','published_year','category']
    valid_items = [1,5,10,20,50,100,500]


    # checking are queries valid or not
    if search_key not in valid_search_keys:
        raise HTTPException(status_code=400, detail=f"Invalid search key '{search_key}', valid keys are {valid_search_keys}")
    if items not in valid_items:
        raise HTTPException(status_code=400, detail=f"You can view books at a time only from these numbers {valid_items}")

    results: list[dict] = []

    for index,each_book_data in enumerate(DATA.values()):
        if len(results) == items:
            break
        if query in each_book_data[search_key].lower():
            results.append(each_book_data)


    return {'results': results}








# route (/new) for adding new books
@app.post('/new')
def new_book(book_data: Book) -> None:
    """ this function will add new data to the dataset """

    if book_data.isbn13 in DATA:
        raise HTTPException(status_code=400, detail=f'Record already found {book_data.isbn13}')
    
    book_data = book_data.model_dump(exclude='isbn13')

    print(book_data)

    return book_data










if __name__ == "__main__":

    print("starting data loading.... ", end = " ")
    data = load_data()
    print("data loaded successfully")
    print(type(data))




