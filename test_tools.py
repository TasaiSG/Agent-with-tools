"""
CSC-128 Assignment 7: tests for the room-booking tools
Tasai Smith-Gandy
"""

from tools import (
    AVAILABILITY,
    AVAILABLE_TOOLS,
    check_availability,
    get_hours,
    book_room,
)


def test_check_availability():
    rooms = check_availability("Monday")

    assert "214" in rooms
    assert "216" in rooms
    assert "220" in rooms


def test_bad_day():
    result = check_availability("Saturday")

    assert "Error" in result


def test_get_hours():
    result = get_hours("Monday")

    assert result == "8:00 AM - 5:00 PM"


def test_bad_hours_day():
    result = get_hours("Sunday")

    assert "Error" in result


def test_book_room():
    result = book_room("Tuesday", "214", "Test Student")

    assert "booked" in result
    assert "214" not in AVAILABILITY["Tuesday"]


def test_cannot_book_unavailable_room():
    result = book_room("Tuesday", "999", "Test Student")

    assert "Error" in result


def test_name_required():
    result = book_room("Wednesday", "216", "")

    assert "Error" in result


def test_available_tools():
    assert "check_availability" in AVAILABLE_TOOLS
    assert "get_hours" in AVAILABLE_TOOLS
    assert "book_room" in AVAILABLE_TOOLS


def test_no_delete_tool():
    assert "delete_room" not in AVAILABLE_TOOLS
    assert "delete" not in AVAILABLE_TOOLS


if __name__ == "__main__":
    test_check_availability()
    test_bad_day()
    test_get_hours()
    test_bad_hours_day()
    test_book_room()
    test_cannot_book_unavailable_room()
    test_name_required()
    test_available_tools()
    test_no_delete_tool()

    print("All tests passed!")
