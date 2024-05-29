from uagents import Context, Model, Protocol

class CancelAppointmentRequest(Model):
    patient_id: int
    doctor_id: int
    slot: str

class CancelAppointmentResponse(Model):
    success: bool

cancel_proto = Protocol()

@cancel_proto.on_message(model=CancelAppointmentRequest, replies=CancelAppointmentResponse)
async def handle_cancel_request(ctx: Context, sender: str, msg: CancelAppointmentRequest):
    doctors = ctx.storage.get("doctors") or {}
    slots = doctors.get(msg.doctor_id, {}).get("available_slots", [])
    slots.append(msg.slot)
    doctors[msg.doctor_id]["available_slots"] = slots
    ctx.storage.set("doctors", doctors)
    await ctx.send(sender, CancelAppointmentResponse(success=True))
