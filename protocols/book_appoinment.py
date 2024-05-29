from uagents import Context, Model, Protocol

class BookAppointmentRequest(Model):
    patient_id: int
    doctor_id: int
    slot: str

class BookAppointmentResponse(Model):
    success: bool

book_proto = Protocol()

@book_proto.on_message(model=BookAppointmentRequest, replies=BookAppointmentResponse)
async def handle_book_request(ctx: Context, sender: str, msg: BookAppointmentRequest):
    # Log the received message
    ctx.logger.info(f"Received booking request: {msg}")

    # Retrieve the list of doctors from storage
    doctors = ctx.storage.get("doctors") or {}
    ctx.logger.info(f"Current doctors in storage: {doctors}")

    # Get the available slots for the specified doctor
    slots = doctors.get(msg.doctor_id, {}).get("available_slots", [])
    ctx.logger.info(f"Available slots for doctor {msg.doctor_id}: {slots}")

    # Check if the requested slot is available
    if msg.slot in slots:
        # Remove the slot from the list of available slots
        slots.remove(msg.slot)
        doctors[msg.doctor_id]["available_slots"] = slots
        ctx.logger.info(f"Updated slots for doctor {msg.doctor_id}: {slots}")

        # Update the doctors information in storage
        ctx.storage.set("doctors", doctors)
        ctx.logger.info(f"Doctors information updated in storage: {doctors}")

        # Send a success response
        await ctx.send(sender, BookAppointmentResponse(success=True))
        ctx.logger.info(f"Sent success response to {sender}")
    else:
        # Send a failure response
        await ctx.send(sender, BookAppointmentResponse(success=False))
        ctx.logger.info(f"Sent failure response to {sender}")

