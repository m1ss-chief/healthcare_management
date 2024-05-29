from uagents import Agent, Context
from uagents.setup import fund_agent_if_low

from protocols.register_patient import register_proto
from protocols.query_appointment import query_proto
from protocols.book_appoinment import book_proto
from protocols.cancel_appointment import cancel_proto
from protocols.first_aid import first_aid_proto
healthcare_agent = Agent(
    name="healthcare_agent",
    port=8002,
    seed="healthcare agent secret phrase",
    endpoint=["http://127.0.0.1:8002/submit"]
)

fund_agent_if_low(healthcare_agent.wallet.address())

healthcare_agent.include(register_proto)
healthcare_agent.include(query_proto)
healthcare_agent.include(book_proto)
healthcare_agent.include(cancel_proto)


# healthcare_agent.include(first_aid_proto)


doctors = {
  1: {"name": "Dr. Smith", "speciality": "Cardiologist","available_slots": ["9:00 AM", "10:00 AM", "11:00 AM"]},
  2: {"name": "Dr. Johnson", "speciality": "Orthologist","available_slots": ["1:00 PM", "2:00 PM", "3:00 PM"]},
  3: {"name": "Dr. Kapoor", "speciality": "Gynecologist","available_slots": ["10:30 AM", "2:30 PM", "4:30 PM"]},
  4: {"name": "Dr. Garcia", "speciality": "Neurologist","available_slots": ["8:00 AM", "11:00 AM", "3:00 PM"]},
  5: {"name": "Dr. Williams", "speciality": "General Physician","available_slots": ["9:15 AM", "12:15 PM", "4:15 PM"]},
}

healthcare_agent._storage.set("doctors", doctors)

@healthcare_agent.on_event("startup")
async def on_startup(ctx: Context):
    ctx.logger.info(f'Healthcare agent started! address {ctx.address}')
    

if __name__ == "__main__":
    healthcare_agent.run()
