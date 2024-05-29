import csv
import os
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from uagents import Model, Protocol
import google.generativeai as genai
from dotenv import load_dotenv,dotenv_values

# config = dotenv_values(".env")
# config = {
#     **dotenv_values(".env"),  # load shared development variables
#     # **dotenv_values(".env.secret"),  # load sensitive variables
#     **os.environ,  # override loaded values with environment variables
# }

load_dotenv() 
# class HealthQuery(Model):
#     query: str

# class HealthResponse(Model):
#     advice: str


class FirstAidQuery(Model):
    ques: str

class FirstAidResponse(Model):
    success:bool
    advice: str

# class MedicineQuery(Model):
#     medicine_name: str

# class MedicineDetails(Model):
#     name: str
#     composition: str
#     uses: str
#     side_effects: str
#     image_url: str
#     manufacturer: str
#     excellent_review_percent: str
#     average_review_percent: str
#     poor_review_percent: str

# genai.configure(api_key=os.getenv("OPENAI_API_KEY"))
genai.configure(api_key=os.environ.get("OPENAIAPI_KEY"))
# The Gemini 1.5 models are versatile and work with both text-only and multimodal prompts
model = genai.GenerativeModel('gemini-1.5-flash-latest')

first_aid_proto = Protocol()


@first_aid_proto.on_message(model=FirstAidQuery, replies=FirstAidResponse)
async def handle_health_query(ctx: Context, sender: str, msg: FirstAidQuery):
    # Call an external API to get health advice
    response = model.generate_content(f"give me first aid for {msg.ques}. your response should be ';' separated with each element in the starting with number. for Example first aid for cuts, response should be in the form of :--- '1. Wash your hands.;2. Apply ointment on it;3. if pain persist visit doctor'  donot include any bold words or sentences in your response")
    print("in firdtsidproto")
    advice = response.text
    ctx.storage.set("firstaidadvice", advice)
    print(advice)
    await ctx.send(sender, FirstAidResponse(success=True,advice=advice))

# @first_aid_proto.on_message(model=HealthQuery, replies=HealthResponse)
# async def handle_health_query(ctx: Context, sender: str, msg: HealthQuery):
#     # Call an external API to get health advice
#     url = "https://health-diagnosis-api.example.com/query"
#     params = {"query": msg.query}
#     headers = {"X-API-Key": "YOUR_HEALTH_DIAGNOSIS_API_KEY"}
#     response = requests.get(url, headers=headers, params=params)
#     advice = response.json().get("advice", "No advice available.")
#     await ctx.send(sender, HealthResponse(advice=advice))

# @first_aid_proto.on_message(model=MedicineQuery, replies=MedicineDetails)
# async def handle_medicine_query(ctx: Context, sender: str, msg: MedicineQuery):
#     with open('medicines.csv', mode='r') as file:
#         csv_reader = csv.DictReader(file)
#         for row in csv_reader:
#             if row["Medicine Name"].lower() == msg.medicine_name.lower():
#                 medicine_details = MedicineDetails(
#                     name=row["Medicine Name"],
#                     composition=row["Composition"],
#                     uses=row["Uses"],
#                     side_effects=row["Side_effects"],
#                     image_url=row["Image URL"],
#                     manufacturer=row["Manufacturer"],
#                     excellent_review_percent=row["Excellent Review %"],
#                     average_review_percent=row["Average Review %"],
#                     poor_review_percent=row["Poor Review %"]
#                 )
#                 await ctx.send(sender, medicine_details)
#                 return
#     await ctx.send(sender, MedicineDetails()) 