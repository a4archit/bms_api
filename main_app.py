"""
BMS-API
======

        I work on this project to make my skills more strong.
"""




# Dependencies
from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import JSONResponse
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


# saving data
def save_data(data: dict) -> None:
    ''' This function will save the provided data '''
    with open('books_data.json', 'w') as file:
        json.dump(data, file)






# extracting current year
current_year = datetime.today().year



# pydantic general model 
class Book(BaseModel):

    title: Annotated[str, Field(..., title='Title', description='Title of book (short text)')]
    isbn13: Annotated[str, Field(..., title='ISBN', description='ISBN number of 13 digits', examples=['9780002005883'], min_length=13, max_length=13)]
    isbn10: Annotated[str, Field(..., title="ISBN 10", description="ISBN 10 is a unique number of 10 digits", examples=['0002005883'])]
    author: Annotated[str, Field(..., title='Author', description='Name of the book author.')]
    thumbnail: Annotated[str, Field(..., title='Thumbnail URL', description='URL of book thumbnail')]
    num_pages: Annotated[int, Field(..., title='Total pages', description='Total number of pages in the book')]
    description: Annotated[str, Field(..., title='Description', description='Description of the book')]
    published_year: Annotated[int, Field(..., gt=0, lt=current_year, title='Published year', description='Published year of the book')]
    
    subtitle: Annotated[Optional[str], Field(title='Subtitle', description='Subtitle of book')] = ""
    category: Annotated[Optional[str], Field(title='Category', description='Category of book')] = ""
    ratings_count: Annotated[Optional[int], Field( title='Total Ratings', description='Total number of reviews given by the readers.')] = None
    average_rating: Annotated[Optional[float], Field(title='Average Rating', description='Average rating of book provide by users')] = None





# pydantic model for data updation
class BookUpdation(BaseModel):

    title:          Annotated[Optional[str], Field(title='Title', description='Title of book (short text)')] = ""
    isbn13:         Annotated[Optional[str], Field(title='ISBN', description='ISBN number of 13 digits', examples=['9780002005883'], min_length=13, max_length=13)] = ""
    isbn10:         Annotated[Optional[str], Field(title="ISBN 10", description="ISBN 10 is a unique number of 10 digits", examples=['0002005883'])] = ""
    author:         Annotated[Optional[str], Field(title='Author', description='Name of the book author.')] = ""
    subtitle:       Annotated[Optional[str], Field(title='Subtitle', description='Subtitle of book')] = ""
    category:       Annotated[Optional[str], Field(title='Category', description='Category of book')] = ""
    thumbnail:      Annotated[Optional[str], Field(title='Thumbnail URL', description='URL of book thumbnail')] = ""
    num_pages:      Annotated[Optional[int], Field(title='Total pages', description='Total number of pages in the book')] = 0
    description:    Annotated[Optional[str], Field(title='Description', description='Description of the book')] = ""
    ratings_count:  Annotated[Optional[int], Field(title='Total Ratings', description='Total number of reviews given by the readers.')] = 0
    published_year: Annotated[Optional[int], Field(gt=0, lt=current_year+1, title='Published year', description='Published year of the book')] = 0
    average_rating: Annotated[Optional[float], Field(title='Average Rating', description='Average rating of book provide by users')] = 0.0







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

    # loading data 
    DATA = load_data()

    if book_data.isbn13 in DATA:
        raise HTTPException(status_code=400, detail=f'Record already found {book_data.isbn13}')
    
    book_nested_data = book_data.model_dump(exclude='isbn13')

    DATA.update({book_data.isbn13: book_nested_data})

    return JSONResponse(status_code = 201, content={'message':'book added succesfully'})





# route (/edit) for updating some information
@app.put('/edit/{isbn13}')
def update_book(isbn13: str, book_latest_data: BookUpdation) :
    """ This function will edit and update the saved records from existing data """
    
    # cheking is isbn13 valid or not
    if len(isbn13) != 13:
        raise HTTPException(status_code=400, detail='Invalid ISBN ID (ISBN ID must be of 13 digits)')
    
    # loading data
    DATA = load_data()
    
    # checking Is given ISBN exists or not
    if isbn13 not in DATA:
        raise HTTPException(status_code=400, detail=f'This ISBN id ({isbn13}) doesn\'t exists.')
    
    existing_book_information: dict = DATA[isbn13]
    updated_book_information: dict = book_latest_data.model_dump(exclude_unset=True) # this will not takes the predefined values (in the pydantic model)

    for key, value in updated_book_information.items():
        existing_book_information[key] = value

    DATA[isbn13] = existing_book_information

    save_data(DATA)

    return JSONResponse(status_code=200, content={'message':f'data updated sucessfully of this isbn id ({isbn13})'})






# route (/delete) for deleting
@app.delete('/delete/{isbn13}')
def delete_book_information(isbn13: str):
    ''' This function will delete the existing book data '''

    # loading data
    DATA = load_data()

    if isbn13 not in DATA:
        raise HTTPException(status_code=404, detail=f'ISBN ({isbn13}) not found in records.')
    
    # deleting book data
    del DATA[isbn13]

    # saving updating data
    save_data(DATA)

    return JSONResponse(status_code=200, content=f'Book deleted successfully ({isbn13})')











if __name__ == "__main__":

    print("starting data loading.... ", end = " ")
    data = load_data()
    print("data loaded successfully")
    print(type(data))

    # 9788445074879


