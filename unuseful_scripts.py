from pydantic import Field, BaseModel, AnyUrl, EmailStr, field_validator, model_validator
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

# print(
#     '\n\n\n',
#     book1,
#     '\n\n\n'
# )



class Address(BaseModel):

    city: str 
    state: str
    pincode: int




class Person(BaseModel):

    name: Annotated[str, Field(..., title="name of person")]
    age: Annotated[int, Field(..., title="Age of person in years")]
    married: Annotated[bool, Field(default=False, title='Person marital status')]
    email: Annotated[str, Field(..., title='Email of person')]
    height: Annotated[float, Field(..., title='Height of person in metres')]
    weight: Annotated[float, Field(..., title='Weight of person in kg')]
    contact: Annotated[Dict[str, str], Field(..., title='Contact informations python dictionary')]
    address: Annotated[Address, Field(..., title='Address of person')]

    # @computed_field
    @property
    def bmi(self) -> float:
        bmi = self.weight/(self.height**2)
        return bmi


    @model_validator(mode='after')
    @classmethod
    def emergency_number_validator(cls, model):
        if model.age > 60 and 'emergency' not in model.contact:
            raise ValueError('Person is older than 60 years and emergency contact not provided yet.')
        return model
    

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['gmail.com','yahoo.com']
        domain_name = value.strip().split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('Not a valid email')
        return value
    

    @field_validator('name')
    @classmethod
    def transform_name(cls, name) -> str:
        return name.upper()

p1_address = Address(**{'city':'meerut','state':'uttar pradesh', 'pincode':298477})
p1_data = {'name':'arpit','age':'64','email':'abc@gmail.com', 
           'contact':{'mob':'8374937584','emergency':'838495748'},
           'weight':'54', 'height':'1.7', 'address': p1_address}

p1 = Person(**p1_data)

print('\n\n',p1)

dict_data = p1.model_dump(exclude={'address':['city']})

print(dict_data)









