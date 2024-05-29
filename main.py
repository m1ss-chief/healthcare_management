import json
import asyncio
import os
from uagents import Model
from uagents.query import query
import uvicorn
import sys
import nest_asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from protocols.book_appoinment import BookAppointmentRequest
from protocols.cancel_appointment import CancelAppointmentRequest
from protocols.first_aid import FirstAidQuery
from protocols.medicine_search import MedicineRequest
from protocols.query_appointment import QueryAppointmentRequest
from protocols.register_patient import RegisterPatientRequest
from agents.user_agent import user_agent
# from backend.bureau import bureau

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

nest_asyncio.apply()
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


AGENT_ADDRESS=user_agent.address
# FIRSR_AID_AGENT_ADDRESS ="agent1qf0ax7vvqz0jh5fhnwd05ynx75t4mzpdse8k8ml8n0skemsw0dedwc9zvja"


@app.get("/get_first_aid")
async def firstaidagent_query(ques:str):
    req=FirstAidQuery(ques=ques)
    print(req)
    response = await query(destination=AGENT_ADDRESS, message=req)
    # print("res",response)
    data = json.loads(response.decode_payload())
    print(data)
    return data

@app.post("/registerPatient")
async def firstaidagent_query(patient:RegisterPatientRequest):
    print(patient)
    response = await query(destination=AGENT_ADDRESS, message=patient)
    # print("res",response)
    data = json.loads(response.decode_payload())
    print(data)
    return data

@app.post("/queryAppointment")
async def queryappointment_query(doctor_id:int):
    print(type(doctor_id))
    req = QueryAppointmentRequest(doctor_id=doctor_id)
    response = await query(destination=AGENT_ADDRESS, message=req)
    # print("res",response)
    data = json.loads(response.decode_payload())
    print(data)
    return data

@app.post("/book_appointment")
async def bookappointment_query(appointment:BookAppointmentRequest):
    # req = BookAppointmentRequest(doctor_id=appointment.doctor_id,)
    response = await query(destination=AGENT_ADDRESS, message=appointment)
    # print("res",response)
    data = json.loads(response.decode_payload())
    print(data)
    return data

@app.post("/cancel_appointment")
async def cancelappointment_query(appointment:CancelAppointmentRequest):
    # req = BookAppointmentRequest(doctor_id=doctor_id)
    response = await query(destination=AGENT_ADDRESS, message=appointment)
    # print("res",response)
    data = json.loads(response.decode_payload())
    print(data)
    return data

@app.get("/medicine_search")
async def medi_query(med:str):
    req = MedicineRequest(medicine_name=med)
    response = await query(destination=AGENT_ADDRESS, message=req)
    # print("res",response)
    data = json.loads(response.decode_payload())
    print(data)
    return data



# async def run_bureau():
#     bureau.run()

# async def run_uvicorn():
#     port = int(os.getenv("PORT", 8000))
#     config = uvicorn.Config(app, host="0.0.0.0", port=port,reload=True)
#     server = uvicorn.Server(config)
#     await server.serve()

# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(
#         asyncio.gather(
#             run_bureau(),
#             run_uvicorn(),
#         )
#     )

# if __name__ == "__main__":
#     port1 = int(os.getenv("PORT", 8000))
#     bureau.run()
#     uvicorn.run(app, host="0.0.0.0", port=port1)

# patient_name="john"
# contact="some addr"
# age=23
# health_problem="dimentis"

# ques= "i have bruise"

# async def agent_query(req):
#     # print(req)
#     response = await query(destination=AGENT_ADDRESS, message=req)
#     print("res",response)
#     data = json.loads(response.decode_payload())
#     return data["text"]


# async def make_agent_call(req: RegisterPatientRequest):
#     try:
#         print("inmake")
#         response = await agent_query(req)
#         return f"successful call - agent response: {response}"
#     except Exception as e:
#         return f'unsuccessful agent call {str(e)}'

# async def firstaidagent_query(req):
#     print(req)
#     response = await query(destination=AGENT_ADDRESS, message=req)
#     # print("res",response)
#     data = json.loads(response.decode_payload())
#     print(data)
#     return response


# async def firstaidmake_agent_call(req: FirstAidQuery):
#     try:
#         print("inmake first aid")
#         response = await firstaidagent_query(req)
#         return f"successful call - agent response"
#     except Exception as e:
#         return f'unsuccessful agent call {str(e)}'  


# if __name__ == "__main__":
    # Create a QueryRequest instance with your query and run make_agent_call with request.
    # request = FirstAidQuery(ques=ques)
    # print(asyncio.run(firstaidmake_agent_call(request)))
    # request = RegisterPatientRequest(patient_name=patient_name, contact=contact, age=age, health_problem=health_problem)
    # print(asyncio.run(make_agent_call(request)))




# import google.generativeai as genai

# genai.configure(api_key="AIzaSyAs1c50xwBsSxQL0HgMb_0FR2K952sg-0w")
# # The Gemini 1.5 models are versatile and work with both text-only and multimodal prompts
# model = genai.GenerativeModel('gemini-1.5-flash-latest')

# response = model.generate_content("give me first aid for bruises. your response should be ';' separated with each element in the starting with number. for Example first aid for cuts, response should be in the form of :--- '1. Wash your hands.;2. Apply ointment on it;3. if pain persist visit doctor'  donot include any bold words or sentences in your response")
# print(response.text)