from uagents import Context, Model, Protocol

class RegisterPatientRequest(Model):
    patient_name: str
    contact: str
    age: int
    health_problem: str

class RegisterPatientResponse(Model):
    success: bool
    patient_id: int

register_proto = Protocol()

@register_proto.on_message(model=RegisterPatientRequest, replies=RegisterPatientResponse)
async def handle_register_request(ctx: Context, sender: str, msg: RegisterPatientRequest):
    print("in register protocl")
    patients = ctx.storage.get("patients") or {}
    patient_id = len(patients) + 1
    patients[patient_id] = {
        "name": msg.patient_name,
        "contact": msg.contact,
        "age": msg.age,
        "health_problem": msg.health_problem
    }
    ctx.storage.set("patients", patients)
    # ctx.loggern("in registerr")
    await ctx.send(sender, RegisterPatientResponse(success=True, patient_id=patient_id))
