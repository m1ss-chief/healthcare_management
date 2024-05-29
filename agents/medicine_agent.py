from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from protocols.register_patient import register_proto
from protocols.query_appointment import query_proto
from protocols.book_appoinment import book_proto
from protocols.cancel_appointment import cancel_proto
from protocols.first_aid import first_aid_proto
from protocols.medicine_search import medicine_proto
medicine_agent = Agent(
    name="medicine_agent",
    port=8003,
    seed="medicine agent secret phrase",
    endpoint=["http://127.0.0.1:8002/submit"]
)

fund_agent_if_low(medicine_agent.wallet.address())

# healthcare_agent.include(register_proto)
# healthcare_agent.include(query_proto)
# healthcare_agent.include(book_proto)
# healthcare_agent.include(cancel_proto)



medicine_agent.include(medicine_proto)


@medicine_agent.on_event("startup")
async def on_startup(ctx: Context):
    ctx.logger.info(f'Healthcare agent started! address {ctx.address}')
    

if __name__ == "__main__":
    medicine_agent.run()
