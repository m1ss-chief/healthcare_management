import csv
import requests
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from uagents import Model, Protocol
from protocols.first_aid import first_aid_proto
import os
import google.generativeai as genai

#
# # The Gemini 1.5 models are versatile and work with both text-only and multimodal prompts
# model = genai.GenerativeModel('gemini-1.5-flash-latest')

firstaid_agent = Agent(
    name="first_aid_agent",
    port=8003,
    seed="first aid agent secret phrase",
    endpoint=["http://127.0.0.1:8003/submit"]
)
# response = model.generate_content("give me first aid for bruises. your response should be ';' separated with each element in the starting with number. for Example first aid for cuts, response should be in the form of :--- '1. Wash your hands.;2. Apply ointment on it;3. if pain persist visit doctor'  donot include any bold words or sentences in your response")
# print(response.text)
fund_agent_if_low(firstaid_agent.wallet.address())

# class HealthQuery(Model):
#     query: str

# class HealthResponse(Model):
#     advice: str

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

# first_aid._storage.set("doctors", doctors)
firstaid_agent.include(first_aid_proto)

@firstaid_agent.on_event("startup")
async def on_startup(ctx: Context):
    ctx.logger.info(f'Firstaid agent started! address {ctx.address}')

if __name__ == "__main__":
    firstaid_agent.run()



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
#     await ctx.send(sender, MedicineDetails())  # Send empty details if medicine not found

