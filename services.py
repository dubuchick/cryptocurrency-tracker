import database as _database
import models as _models
import sqlalchemy.orm as _orm
import email_validator as _email_validator
import passlib.hash as _hash
import jwt as _jwt
import fastapi as _fastapi
import fastapi.security as _security
import schemas as _schemas

_JWT_SECRET = "thisistemporary"

oauth2schema = _security.OAuth2PasswordBearer("/token")

def _create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_user_by_email(email: str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first()

async def get_coin_by_name(name: str, db: _orm.Session):
    return db.query(_models.TrackedCoin).filter(_models.TrackedCoin.name == name).first()

async def create_user(user : _schemas.UserCreate, db: _orm.Session):
    if user.password_confrimation != user.password:
        raise _fastapi.HTTPException(
            status_code=401, detail="Password doesn't match"
        )
    hashed_password = _hash.bcrypt.hash(user.password)
    user_obj = _models.User(email=user.email, hashed_password=hashed_password)

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

async def create_token(user: _models.User):
    user_schema_obj = _schemas.User.from_orm(user)

    user_dict = user_schema_obj.dict()

    token = _jwt.encode(user_dict,_JWT_SECRET)

    return dict(access_token=token, token_type="bearer")

async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(email=email,db=db)

    if not user:
        return False
    
    if not user.verify_password(password=password):
        return False
    
    return user

async def get_current_user(db: _orm.Session=_fastapi.Depends(get_db),token: str=_fastapi.Depends(oauth2schema)):
    try:
        payload = _jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid credentials"
        )
    return _schemas.User.from_orm(user)

async def add_coin(user: _schemas.User, db: _orm.Session, coin: _schemas.TrackerCoinCreate):
    coin = _models.TrackedCoin(**coin.dict())
    db.add(coin)
    db.commit()
    db.refresh(coin)

    return _schemas.TrackerCoin.from_orm(coin)

async def get_coins(user: _schemas.User, db:_orm.Session):
    coins = db.query(_models.TrackedCoin)

    return list(map(_schemas.TrackerCoin.from_orm, coins))

async def delete_coin(user: _schemas.User,name:str, db:_orm.Session):
    coin = await get_coin_by_name(name,db)
    print(coin)
    if not coin:
        raise _fastapi.HTTPException(
            status_code=404, detail="Coin not found"
        )
    db.delete(coin)
    db.commit()
    return {"ok":True}
