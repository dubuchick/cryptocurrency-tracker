import pydantic as _pydantic

class _UserBase(_pydantic.BaseModel):
    email: str

class UserCreate(_UserBase):
    password: str
    password_confrimation: str

    class Config:
        from_attributes = True

class User(_UserBase):
    id: int

    class Config:
        from_attributes = True

class _TrackerCoinBase(_pydantic.BaseModel):
    name : str
    price : float

class TrackerCoinDelete(_TrackerCoinBase):
    name : str

class TrackerCoinCreate(_TrackerCoinBase):
    name : str
    price : float
    
    class Config:
        from_attributes = True

class TrackerCoin(_TrackerCoinBase):
    id: int
    
    class Config:
        from_attributes = True