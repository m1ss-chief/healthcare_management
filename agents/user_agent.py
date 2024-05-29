from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from agents.healthcare_agent import healthcare_agent
from agents.first_aid_agent import firstaid_agent
from agents.medicine_agent import medicine_agent
from protocols.first_aid import FirstAidQuery, FirstAidResponse
from protocols.medicine_search import MedicineRequest, MedicineResponse
from protocols.register_patient import RegisterPatientRequest, RegisterPatientResponse
from protocols.query_appointment import QueryAppointmentRequest, QueryAppointmentResponse
from protocols.book_appoinment import BookAppointmentRequest, BookAppointmentResponse
from protocols.cancel_appointment import CancelAppointmentRequest, CancelAppointmentResponse

# HEALTHCARE_AGENT_ADDRESS = "agent1qtyy2cxunv0tatsvge7keatp48mpwty57ecfgwehzsgp2yyhzlz7jze6qht"
HEALTHCARE_AGENT_ADDRESS = healthcare_agent.address
FIRSR_AID_AGENT_ADDRESS = firstaid_agent.address
MEDICINE_AID_AGENT_ADDRESS = medicine_agent.address

user_agent = Agent(
    name="user_agent",
    # port=8001,
    seed="user agent secret phrase",
    # endpoint=["http://127.0.0.1:8001/submit"]
)



fund_agent_if_low(user_agent.wallet.address())

@user_agent.on_event("startup")
async def on_startup(ctx: Context):
    ctx.logger.info(f'User agent started!,{ctx.address}   ')


# async def register_patient(ctx: Context, name: str, contact: str, age: int, health_problem: str):
#     request = RegisterPatientRequest(patient_name=name, contact=contact, age=age, health_problem=health_problem)
#     await ctx.send(HEALTHCARE_AGENT_ADDRESS, request)

@user_agent.on_query(model=FirstAidQuery,replies=FirstAidQuery)
async def give_firstaid(ctx:Context,sender:str,msg:FirstAidQuery):
    ctx.logger.info("in first aid")
    print("in first iad")
    # print(sender)
    ctx.storage.set("mysender",sender)
    request=FirstAidQuery(ques=msg.ques)
    res=await ctx.send(FIRSR_AID_AGENT_ADDRESS,request)
    # print(res.status.value)
    # if(res.status=='DeliveryStatus.DELIVERED'):
    #     print("delivered")
    # advice=ctx.storage.get("firstaidadvice")
    # print(advice)
    # await ctx.send(sender,FirstAidResponse(advice=advice,success=True))

@user_agent.on_message(FirstAidResponse)
async def handle_givefirstaid_response(ctx: Context, sender: str, msg: FirstAidResponse):
    # print(msg)
    # print(sender)
    if msg.success:
        mysender=ctx.storage.get("mysender")
        print("myswnder",mysender)
        ctx.logger.info(f"{msg.advice}")
        await ctx.send(mysender,msg)
    else:
        ctx.logger.info("First Aid not given.")
        await ctx.send(mysender,FirstAidResponse(advice="First Aid not given.",success=True))

#########query register patiemt############
@user_agent.on_query(model=RegisterPatientRequest,replies=RegisterPatientRequest)
async def register_patient(ctx: Context,sender:str,msg:RegisterPatientRequest):
    ctx.logger.info("in register")
    # ctx.logger.info(msg)
    ctx.storage.set("mysender",sender)
    request = RegisterPatientRequest(patient_name=msg.patient_name, contact=msg.contact, age=msg.age, health_problem=msg.health_problem)
    # ctx.logger.info(request)
    await ctx.send(HEALTHCARE_AGENT_ADDRESS, request)

@user_agent.on_message(RegisterPatientResponse)
async def handle_register_response(ctx: Context, sender: str, msg: RegisterPatientResponse):
    if msg.success:
        ctx.logger.info(f"Patient registered successfully with ID: {msg.patient_id}")
        mysender=ctx.storage.get("mysender")
        await ctx.send(mysender,msg)
    else:
        ctx.logger.info("Patient registration failed.")


############query appointment#############
@user_agent.on_query(model=QueryAppointmentRequest,replies=QueryAppointmentRequest)
async def query_appointment(ctx: Context,sender:str, msg: QueryAppointmentRequest):
    ctx.storage.set("mysender",sender)
    request = QueryAppointmentRequest(doctor_id=msg.doctor_id)
    await ctx.send(HEALTHCARE_AGENT_ADDRESS, request)

@user_agent.on_message(QueryAppointmentResponse)
async def handle_query_response(ctx: Context, sender: str, msg: QueryAppointmentResponse):
    ctx.logger.info(f"Available slots: {msg.available_slots}")
    await ctx.send(ctx.storage.get("mysender"),msg)



##############book appointment#########
@user_agent.on_query(model=BookAppointmentRequest,replies=BookAppointmentRequest)
async def book_appointment(ctx: Context,sender:str, msg:BookAppointmentRequest):
    ctx.storage.set("mysender",sender)
    print(msg)
    request = BookAppointmentRequest(patient_id=msg.patient_id, doctor_id=msg.doctor_id, slot=msg.slot)
    await ctx.send(HEALTHCARE_AGENT_ADDRESS, request)

@user_agent.on_message(BookAppointmentResponse)
async def handle_book_response(ctx: Context, sender: str, msg: BookAppointmentResponse):
    if msg.success:
        ctx.logger.info("Appointment booked successfully.")
        await ctx.send(ctx.storage.get("mysender"),msg)
    else:
        ctx.logger.info("Failed to book appointment.")
        await ctx.send(ctx.storage.get("mysender"),msg)



############cancel appointment#################
@user_agent.on_query(model=CancelAppointmentRequest,replies=CancelAppointmentRequest)
async def cancel_appointment(ctx: Context,sender:str, msg:CancelAppointmentRequest):
    ctx.storage.set("mysender",sender)
    request = CancelAppointmentRequest(patient_id=msg.patient_id, doctor_id=msg.doctor_id, slot=msg.slot)
    await ctx.send(HEALTHCARE_AGENT_ADDRESS, request)

@user_agent.on_message(CancelAppointmentResponse)
async def handle_cancel_response(ctx: Context, sender: str, msg: CancelAppointmentResponse):
    if msg.success:
        ctx.logger.info("Appointment canceled successfully.")
        await ctx.send(ctx.storage.get("mysender"),msg)
    else:
        ctx.logger.info("Failed to cancel appointment.")
        await ctx.send(ctx.storage.get("mysender"),msg)


################### medicine search ##########
@user_agent.on_query(model=MedicineRequest,replies=MedicineRequest)
async def cancel_appointment(ctx: Context,sender:str, msg:MedicineRequest):
    ctx.storage.set("mysender",sender)
    request = MedicineRequest(medicine_name=msg.medicine_name)
    await ctx.send(MEDICINE_AID_AGENT_ADDRESS, request)

@user_agent.on_message(MedicineResponse)
async def handle_cancel_response(ctx: Context, sender: str, msg: MedicineResponse):
    # if msg.success:
    ctx.logger.info("Medicine data fetched successfully.")
    print(msg)
    await ctx.send(ctx.storage.get("mysender"),msg)
    # else:
    #     ctx.logger.info("Medicine data fetched appointment.")
    #     await ctx.send(ctx.storage.get("mysender"),msg)



#####run########
if __name__ == "__main__":
    user_agent.run()
