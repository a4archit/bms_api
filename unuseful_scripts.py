from pydantic import Field, BaseModel, AnyUrl, EmailStr
from typing import List, Dict, Optional, Annotated
from datetime import datetime


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



book1_data = {
    'isbn13': '2984786989766',
    'isbn10':'8374758473',
    'title':'demo book',
    'author':'no-name',
    'thumbnail':'https://www.dummyurl.com/invalid', 
    'num_pages':290, 
    'description':'-description will be here-', 
    'published_year':2013,
    'ratings_count': 234
              
}

book1 = Book(**book1_data)

print(
    '\n\n\n',
    book1,
    '\n\n\n'
)





