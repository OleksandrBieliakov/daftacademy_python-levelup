from fastapi import FastAPI, Request, HTTPException

from pydantic import BaseModel

app = FastAPI()
# to see what funny will come
app.counter = 0
app.next_patient_id = 0
app.patients = dict()


class Patient(BaseModel):
    name: str
    surename: str


class PatientResp(BaseModel):
    id: int
    patient: Patient


class HelloResp(BaseModel):
    message: str


class GiveMeSomethingRq(BaseModel):
    first_key: str


class GiveMeSomethingResp(BaseModel):
    received: dict
    constant_data: str = "python jest super"


class MethodResp(BaseModel):
    method: str


@app.get("/", response_model=HelloResp)
def root():
    return HelloResp(message="Hello World during the coronavirus pandemic!")


@app.post("/giveme", response_model=GiveMeSomethingResp)
def receive_something(rq: GiveMeSomethingRq):
    return GiveMeSomethingResp(received=rq.dict())


@app.get('/counter')
def counter():
    app.counter += 1
    return app.counter


@app.get("/hello/{name}", response_model=HelloResp)
async def read_item(name: str):
    return HelloResp(message=f"Hello {name}")


@app.get("/method", response_model=MethodResp)
@app.post("/method", response_model=MethodResp)
@app.put("/method", response_model=MethodResp)
@app.delete("/method", response_model=MethodResp)
def method(req: Request):
    return MethodResp(method=req.method)


@app.post("/patient", response_model=PatientResp)
def post_patient_with_id(req: Patient):
    app.next_patient_id += 1
    patient_id = app.next_patient_id
    app.patients[patient_id] = req
    return PatientResp(id=patient_id, patient=req.dict())


@app.get("/patient/{patient_id}", response_model=Patient)
def get_patient(patient_id: int):
    if not patient_id in app.patients:
        raise HTTPException(status_code=204, detail="Patient not found")
    return app.patients[patient_id]