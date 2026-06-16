from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='Name of the Patient', description='Less than 50 characters', examples=['Raina'])]
    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=0, lt=120)
    weight: Annotated[float, Field(gt=0, strict=True)]
    height_cm: int = Field(gt=0, description="Height in centimeters") 
    married: Annotated[Optional[bool], Field(default=None, description='Is the person married or not')] = None
    allergies: Optional[list[str]] = None
    contact_details: dict[str, str]

    @computed_field
    @property
    def calculated_bmi(self) -> float:
        height_meters = self.height_cm / 100
        return round(self.weight / (height_meters ** 2), 2)

    @field_validator('email')
    @classmethod
    def email_validator(cls, value: str) -> str:
        valid_domains = ['hdfc.com', 'icici.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        return value
    
    @field_validator('name')
    @classmethod
    def transform_name(cls, value: str) -> str:
        return value.upper()
    
    @model_validator(mode='after')
    def validate_emergency_contact(self) -> 'Patient':
        if self.age > 60 and 'emergency' not in self.contact_details:
            raise ValueError('Patients Older than 60 must have emergency contact')
        return self


def update_patient_data(patient: Patient):
    print(f"Name: {patient.name}")
    print(f"Age: {patient.age}")
    print(f"Weight: {patient.weight} kg")
    print(f"Height: {patient.height_cm} cm")
    print(f"Married: {patient.married}")
    print(f"Allergies: {patient.allergies}")
    print(f"Contact: {patient.contact_details}")
    print(f"LinkedIn: {str(patient.linkedin_url)}") # Casted to str for safety
    print(f"BMI: {patient.calculated_bmi}")
    print('--> Status: Updated successfully')    

# Input Data
patient_info = {
    'name': 'raina',
    'email': 'abc@icici.com',
    'linkedin_url': 'https://linkedin.com',
    'age': 65,
    'weight': 50.0, 
    'height_cm': 160, 
    'married': False,
    'allergies': ['pollen', 'dust'],
    'contact_details': {'phone_no': '231407', 'emergency': '4521087'}
}

# Execution
patient1 = Patient(**patient_info)
update_patient_data(patient1)
