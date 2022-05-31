import time

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from neo4j import GraphDatabase, exceptions

from db_object_classes.relationship import Relationship
from db_object_classes.type import Type
from src.settings import settings
from routers import router

from src.db_object_classes.base import Base
from src.db_object_classes.desk import Desk


app = FastAPI()

DRIVER = None

# Все пути будут обозначаться тут
app.include_router(router)


# Подключение к БД
@app.on_event('startup')
def startup():
    for i in range(1, 5):
        try:
            global DRIVER
            DRIVER = GraphDatabase.driver(
                settings.database_url,
                auth=(settings.database_url_login, settings.database_url_password)
            )
            DRIVER.verify_connectivity()
            Base.driver = DRIVER
            a = Relationship.driver
            b = Type.driver
            break
        except exceptions.ServiceUnavailable as e:
            print(f'Could not connect to database. Attempt {i}. Error message: "{e}"')
            time.sleep(1)
        except Exception as e:
            if DRIVER is not None:
                DRIVER.close()
            raise e
    else:
        if DRIVER is not None:
            DRIVER.close()
        raise Exception('Could not connect to database')


@app.on_event('shutdown')
def shutdown():
    print(1)
    try:
        global DRIVER
        if DRIVER is not None:
            DRIVER.close()
    except Exception as e:
        print(str(e))


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


# Запуск приложение через этот файл
if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=settings.server_host,
        port=settings.server_port,
        workers=4,
        reload=True
    )

