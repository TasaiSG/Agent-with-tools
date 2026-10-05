import json
from groq import Groq

from tools import AVAILABLE_TOOLS, TOOL_SCHEMAS


MODEL = "openai/gpt-oss-120b"
MAX_ROUNDS = 5

client = Groq()


def dispatch_tool(tool_name, arguments):
    """Validate and safely execute a requested tool."""

    # Validate the name BEFORE looking up or executing anything.
    if tool_name not in AVAILABLE_TOOLS:
        return {
            "error": f"Unknown tool: {tool_name}",
            "executed": False,
        }

    try:
        result = AVAILABLE_TOOLS[tool_name](**arguments)

        return {
            "result": result,
            "executed": True,
        }

    except Exception as exc:
        # Tool errors become tool results instead of crashing the conversation.
        return {
            "error": str(exc),
            "executed": False,
        }


def run_agent(messages, confirmed=False):
    """
    Run the agent and its tools.

    messages should contain the conversation history.
    confirmed=True is required before book_room can actually run.
    """

    conversation = list(messages)

    for _ in range(MAX_ROUNDS):

        response = client.chat.completions.create(
            model=MODEL,
            messages=conversation,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message

        # No tool call: return the model's normal answer.
        if not assistant_message.tool_calls:
            return assistant_message.content, conversation

        # Add the assistant's tool request to the conversation.
        conversation.append(assistant_message)

        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name

            # Safely parse the model's JSON arguments.
            try:
                arguments = json.loads(tool_call.function.arguments)

            except (json.JSONDecodeError, TypeError):
                tool_result = {
                    "error": "Malformed JSON arguments.",
                    "executed": False,
                }

                conversation.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result),
                })

                continue

            # book_room changes state, so require explicit confirmation.
            if tool_name == "book_room" and not confirmed:
                confirmation = (
                    "The agent wants to book a room with these details:\n"
                    f"{json.dumps(arguments, indent=2)}\n\n"
                    "Do you want me to proceed? Please answer yes or no."
                )

                return confirmation, conversation

            # Safely dispatch the tool.
            tool_result = dispatch_tool(tool_name, arguments)

            conversation.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result),
            })

        # Continue the loop so the model can see the tool result.

    return (
        "I reached the maximum number of tool calls for this request.",
        conversation,
    )
