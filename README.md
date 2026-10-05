# CSC-128 Tool Agent

This project is a Streamlit-based tool agent created for CSC-128 Assignment 7.

The agent can use three tools:

- `check_availability` — checks which rooms are available on a weekday.
- `get_hours` — checks the facility's opening hours.
- `book_room` — reserves an available room.

The `book_room` tool is a state-changing action, so the application requires explicit confirmation before making a booking.

## Files

- `tools.py` — contains the three tools and their JSON schemas.
- `agent.py` — contains the tool-calling loop and tool dispatch logic.
- `app.py` — contains the Streamlit user interface and tool call log.
- `test_tools.py` — contains tests for the tools and dispatch behavior.
- `requirements.txt` — lists the required Python packages.
- `.streamlit/secrets.toml` — stores the Groq API key locally and is not committed to Git.

## Setup

Create and activate a Python virtual environment, then install the required packages:

```bash
pip install -r requirements.txt
