"""
CSC-128 Assignment 7 starter: the tools and their schemas
Tasai Smith-Gandy
"""

AVAILABILITY = {
    "Monday": ["214", "216", "220"],
    # TODO 1: fill in the rest of the week
    "Tuesday": ["214", "218", "220"],
    "Wednesday": ["216", "218"],
    "Thursday": ["214", "216", "220"],
    "Friday": ["218", "220"],
}


def check_availability(day):
    """TODO 2: return which rooms are free. Handle a bad day name."""
    if day not in AVAILABILITY:
        return f"Error: {day} is not a valid weekday."

    return AVAILABILITY[day]


def get_hours(day):
    """TODO 3: return the opening hours for a weekday."""
    hours = {
        "Monday": "8:00 AM - 5:00 PM",
        "Tuesday": "8:00 AM - 5:00 PM",
        "Wednesday": "8:00 AM - 5:00 PM",
        "Thursday": "8:00 AM - 5:00 PM",
        "Friday": "8:00 AM - 5:00 PM",
    }

    if day not in hours:
        return f"Error: {day} is not a valid weekday."

    return hours[day]


def book_room(day, room, name):
    """
    TODO 4: reserve a room and remove it from availability.

    Think about what this function should NOT be able to do before you
    write it. Do not add a delete function.
    """
    if day not in AVAILABILITY:
        return f"Error: {day} is not a valid weekday."

    if room not in AVAILABILITY[day]:
        return f"Error: Room {room} is not available on {day}."

    if not name or not name.strip():
        return "Error: A name is required."

    AVAILABILITY[day].remove(room)

    return f"Room {room} booked for {name} on {day}."


AVAILABLE_TOOLS = {
    # TODO 5: map every tool name to its function
    "check_availability": check_availability,
    "get_hours": get_hours,
    "book_room": book_room,
}


# TODO 6: write a JSON schema for each tool. The description field is
# instruction, not documentation. Write it as though you were telling a new
# employee when to use this form.
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": (
                "Use this when the user wants to know which rooms "
                "are currently available on a specific weekday."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "day": {
                        "type": "string",
                        "description": (
                            "The weekday to check, such as Monday."
                        ),
                    }
                },
                "required": ["day"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_hours",
            "description": (
                "Use this when the user asks what hours the facility "
                "is open on a specific weekday."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "day": {
                        "type": "string",
                        "description": (
                            "The weekday whose hours should be checked."
                        ),
                    }
                },
                "required": ["day"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "book_room",
            "description": (
                "Use this when the user wants to reserve an available "
                "room. Confirm the booking with the user before calling "
                "this tool because it changes room availability."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "day": {
                        "type": "string",
                        "description": (
                            "The weekday for the reservation."
                        ),
                    },
                    "room": {
                        "type": "string",
                        "description": (
                            "The room number to reserve."
                        ),
                    },
                    "name": {
                        "type": "string",
                        "description": (
                            "The name of the person making the reservation."
                        ),
                    },
                },
                "required": ["day", "room", "name"],
            },
        },
    },
]
