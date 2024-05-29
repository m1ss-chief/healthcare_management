# Healthcare Management System

This Healthcare Management System is designed to handle patient registration, appointment scheduling, and provide first aid advice using a multi-agent system built with `uAgents`. The system consists of several protocols and agents to manage different aspects of healthcare services.

## Components

### Protocols

- `book_appointment.py`: Defines the protocol for booking appointments.
- `cancel_appointment.py`: Defines the protocol for canceling appointments.
- `query_appointment.py`: Defines the protocol for querying available appointment slots.
- `register_patient.py`: Defines the protocol for registering new patients.
- `first_aid.py`: Defines the protocol for first aid queries.
- `medicine_search.py`: Defines the protocol for querying about any specific medicine.

### Agents

- `healthcare_agent.py`: Manages doctor's availability and handles all healthcare-related protocols.
- `user_agent.py`: Handles patient registration, queries for available slots, booking, and canceling appointments.
- `first_aid_agent.py`: Provides a quick first aid advice.
- `medicine_agent.py`: Provides a detailed information about medicines.


## Setup Instructions

### Prerequisites

- Python 3.8 or above
- `uAgents` library

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/healthcare_management.git
   cd healthcare_management
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Rename .env_example to .env input
   ```bash
   OPENAPI_KEY = <YOUR_OWN_API_KEY>
   ```
   You can get your own APIKEY from [here](https://aistudio.google.com/app/apikey).

### Running the Agents

1. Start all the Agents together:
   ```bash
   python bureau.py
   ```
2. Start the uvicorn server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 
### Usage

- **Register Patient**: Use the User Agent to register a new patient.
- **Query Appointments**: Query the Healthcare Agent for available appointment slots.
- **Book Appointment**: Book an appointment through the Healthcare Agent.
- **Cancel Appointment**: Cancel an existing appointment via the Healthcare Agent.
- **First Aid Advice**: Query the First Aid Agent for common first aid advice.
- **Medicine Information**: Query the First Aid Agent for detailed information about a specific medicine.
