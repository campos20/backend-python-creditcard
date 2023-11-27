from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from config.env_var_config import DB_ADDRESS, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
