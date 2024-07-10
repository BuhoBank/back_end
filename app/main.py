from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .models import CustomerModel, LogInModel
from .crud import add_customer
from .crud import checkData
from fastapi.encoders import jsonable_encoder


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/register_user", response_description="Add new customer", response_model=CustomerModel)
async def create_customer(customer: CustomerModel):
    try:
        new_customer = await add_customer(customer)
        if new_customer:
            new_customer = jsonable_encoder(new_customer)
        
        return JSONResponse(status_code=201, content=new_customer)
    except ValueError as e:
        #Code=400 usuario ci o email ya existe.
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/log_in", response_model=dict)
async def logIn (Credentials: LogInModel):
    authenticate = await checkData(Credentials)
    response_data = {"authenticated": authenticate}

    # Convierte el diccionario en JSON serializable
    response_json = jsonable_encoder(response_data)

    # Devuelve la respuesta como JSONResponse
    return JSONResponse(status_code=201, content=response_json)
