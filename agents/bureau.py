
from uagents import Agent, Bureau, Context, Model, Protocol
import sys
import os
from agents.user_agent import user_agent
from agents.healthcare_agent import healthcare_agent
from agents.first_aid_agent import firstaid_agent
from agents.medicine_agent import medicine_agent

port2 = int(os.getenv("PORT", 8004))
bureau = Bureau(port=port2,endpoint=f'http://localhost:{port2}/submit')

bureau.add(user_agent)
bureau.add(healthcare_agent)
bureau.add(firstaid_agent)
bureau.add(medicine_agent)

# bureau.add(user_agent)

if __name__ == "__main__":
    bureau.run()