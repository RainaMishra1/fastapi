from pydantic import BaseModel

class Address(BaseModel):
    city:str
    state:str
    pin:str


class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address:Address

address_dict={'city':'Mumbai','state':'maharashtra','pin':'421038'}    

address1=Address(**address_dict)

patient_dict={'name':'Raina','gender':'female','age':21,'address':address1}

patient1=Patient(**patient_dict)

temp=patient1.model_dump(include=['name']) #we can use exclude also.
print(temp)
print(type(temp))
