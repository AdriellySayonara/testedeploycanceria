#celery -A src.config.celery_worker worker -l info -P eventlet

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel

from src import crud, models, schemas
import database
from database import engine
from src.routes.api import router as api_router

def insert_initial_values():
	db = database.SessionLocal()
	userTeste = schemas.UserCreate(name='rian', email= 'riantal@gmail.com', numCRM= '123', password='teste123')
	crud.create_user(db=db, user=userTeste)
	classifierTeste = schemas.ClassifierBase(name='Rede Neural Mobile CNN', path= 'my_model', labels= '["Cancer","Nao-Cancer"]', type=models.ClassifierEnum.savedmodel)
	crud.create_classifier(db=db, classifier=classifierTeste)
	db.close()

if not engine.table_names():
	models.Base.metadata.create_all(bind=engine)
	insert_initial_values()

app = FastAPI()

app.include_router(api_router)


# in production you can use Settings management
# from pydantic to get secret key from .env
class Settings(BaseModel):
	authjwt_secret_key: str = "KID BEMGALA"


# callback to get your configuration
@AuthJWT.load_config
def get_config():
	return Settings()


# exception handler for authjwt
# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
	return JSONResponse(
		status_code=401,
		content={"detail": "Unauthorized"}
	)





'''
			async with aiofiles.open(os.path.join('static', filename), mode='wb') as out_file:
		content = await in_file.read()  # async read
		image = Image.open(io.BytesIO(content))
		image.save(os.path.join('staticPIL', 'teste'),"JPEG")
		await out_file.write(content)  # async write
	'''

