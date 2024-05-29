from typing import List
from uagents import Context, Model, Protocol
from pathlib import Path
import json

# Define medicine data path (replace with your actual file path)
medicine_data_path = "medicine_data.json"
data_path = Path(__file__).parent / "medicine_data.json"
print("path",data_path)
with open(data_path, "r") as f:
    medicine_data = json.load(f)

class MedicineRequest(Model):
    medicine_name: str

class MedicineModel(Model):
    MedicineName:str
    Composition: str
    Uses:str
    Side_effects:str
    Manufacturer:str

class MedicineResponse(Model):
    medicine_data:List[MedicineModel]

medicine_proto = Protocol()

@medicine_proto.on_message(model=MedicineRequest, replies=MedicineResponse)
async def handle_query_request(ctx: Context, sender: str, msg: MedicineRequest):
    
    res = [val for key, val in medicine_data.items() if msg.medicine_name in key]
    newdata = [{"MedicineName":item["Medicine Name"],"Composition": item["Composition"], "Uses": item["Uses"], "Side_effects": item["Side_effects"], "Manufacturer": item["Manufacturer"]}
    for item in res]
        
    print(newdata)
    await ctx.send(sender, MedicineResponse(medicine_data=newdata))
