import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
from typing import List
import httpx as _httpx
import requests as _requests

import schemas as _schemas
import services as _services

app = _fastapi.FastAPI()

# Signup 
@app.post("/users")
async def create_user(
    user: _schemas.UserCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = await _services.get_user_by_email(email=user.email, db=db)
    if db_user:
        raise _fastapi.HTTPException(
            status_code=400,detail="Email has already been registered"
        )
    user = await _services.create_user(user=user, db=db)

    return await _services.create_token(user=user)

# Signin
@app.post("/token")
async def generate_token(form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(), 
                         db: _orm.Session = _fastapi.Depends(_services.get_db)):
    user = await _services.authenticate_user(
        email=form_data.username, password=form_data.password, db=db
    )

    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")
    
    return await _services.create_token(user=user)

# Get current user
@app.get("/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user

# Import the data
@app.get("/insert/data")
async def insert_data(db:_orm.Session= _fastapi.Depends(_services.get_db)):
    return await _services.insert_data(db=db)

# Add coins to tracker
@app.post("/coins", response_model=_schemas.TrackerCoin)
async def add_coin(
    trackercoin: _schemas.TrackerCoinCreate, 
    user: _schemas.User = _fastapi.Depends(_services.get_current_user), 
    db:_orm.Session= _fastapi.Depends(_services.get_db)):
    return await _services.add_coin(user=user,db=db,coin=trackercoin)

# Get list of coins
@app.get("/capcoin/coins", response_model=List[_schemas.Coins])
async def get_coins(user: _schemas.User = _fastapi.Depends(_services.get_current_user),db:_orm.Session= _fastapi.Depends(_services.get_db)):
    return await _services.get_capcoin_coins(user=user,db=db)

# Delete Coin
@app.delete("/coin/delete")
async def delete_coin(
    coin: _schemas.TrackerCoinDelete,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user), 
    db:_orm.Session= _fastapi.Depends(_services.get_db)
):
    return await _services.delete_coin(user=user,name=coin.name,db=db)