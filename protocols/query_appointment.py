from typing import List
from uagents import Context, Model, Protocol

class QueryAppointmentRequest(Model):
    doctor_id: int

class QueryAppointmentResponse(Model):
    available_slots: List[str]
    name:str
    speciality:str

query_proto = Protocol()

@query_proto.on_message(model=QueryAppointmentRequest, replies=QueryAppointmentResponse)
async def handle_query_request(ctx: Context, sender: str, msg: QueryAppointmentRequest):
    doctors = ctx.storage.get("doctors") or {}
    slots = doctors.get(msg.doctor_id, {}).get("available_slots", [])
    speciality = doctors.get(msg.doctor_id, {}).get("speciality", "")
    name = doctors.get(msg.doctor_id, {}).get("name", "")
    await ctx.send(sender, QueryAppointmentResponse(available_slots=slots,name=name,speciality=speciality))
