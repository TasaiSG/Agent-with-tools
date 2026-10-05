import os
import json
import streamlit as st


# Load the Groq API key from Streamlit secrets.
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

from agent import run_agent


st.set_page_config(
    page_title="CSC-128 Tool Agent",
    page_icon="🤖",
)

st.title("🤖 CSC-128 Tool Agent")
st.write("Ask the agent something that may require one of its tools.")


# Keep conversation and pending confirmation between Streamlit reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_messages" not in st.session_state:
    st.session_state.pending_messages = None

if "tool_log" not in st.session_state:
    st.session_state.tool_log = []


# Display previous conversation.
for message in st.session_state.messages:
    role = message.get("role")

    if role in ("user", "assistant"):
        with st.chat_message(role):
            st.write(message.get("content", ""))


# Display the tool log.
st.subheader("Tool Call Log")

if not st.session_state.tool_log:
    st.caption("No tools have been called yet.")
else:
    for i, call in enumerate(st.session_state.tool_log, start=1):
        with st.expander(f"Tool call {i}: {call['name']}"):
            st.write("**Arguments:**")
            st.code(json.dumps(call["arguments"], indent=2))

            st.write("**Result:**")
            st.code(json.dumps(call["result"], indent=2))


# User input.
prompt = st.chat_input("Ask me something...")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
    })

    with st.chat_message("user"):
        st.write(prompt)

    # Run the agent.
    answer, conversation = run_agent(
        st.session_state.messages,
        confirmed=False,
    )

    # Look through the conversation for tool calls and results.
    for i, message in enumerate(conversation):

        if hasattr(message, "tool_calls") and message.tool_calls:
            for tool_call in message.tool_calls:

                try:
                    arguments = json.loads(
                        tool_call.function.arguments
                    )
                except (json.JSONDecodeError, TypeError):
                    arguments = {
                        "error": "Malformed JSON arguments"
                    }

                # Look for the matching tool result.
                result = None

                for later_message in conversation[i + 1:]:
                    if (
                        isinstance(later_message, dict)
                        and later_message.get("role") == "tool"
                        and later_message.get("tool_call_id")
                        == tool_call.id
                    ):
                        try:
                            result = json.loads(
                                later_message.get("content", "{}")
                            )
                        except json.JSONDecodeError:
                            result = later_message.get("content")

                        break

                # Don't duplicate an existing log entry.
                already_logged = any(
                    item["name"] == tool_call.function.name
                    and item["arguments"] == arguments
                    for item in st.session_state.tool_log
                )

                if not already_logged:
                    st.session_state.tool_log.append({
                        "name": tool_call.function.name,
                        "arguments": arguments,
                        "result": result,
                    })

    # Check whether a booking confirmation is needed.
    if (
        ("book" in answer.lower() or "reserve" in answer.lower())
        and (
            "proceed" in answer.lower()
            or "confirm" in answer.lower()
            or "would you like" in answer.lower()
        )
    ):
        st.session_state.pending_messages = conversation

        with st.chat_message("assistant"):
            st.write(answer)

    else:
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
        })

        with st.chat_message("assistant"):
            st.write(answer)


# Confirmation section.
if st.session_state.pending_messages is not None:

    st.warning(
        "A state-changing action is waiting for your confirmation."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Yes, proceed"):

            confirmed_messages = list(
                st.session_state.pending_messages
            )

            confirmed_messages.append({
                "role": "user",
                "content": "Yes, proceed with the booking.",
            })

            answer, conversation = run_agent(
                confirmed_messages,
                confirmed=True,
            )

            # Log any tool calls made after confirmation.
            for i, message in enumerate(conversation):

                if hasattr(message, "tool_calls") and message.tool_calls:
                    for tool_call in message.tool_calls:

                        try:
                            arguments = json.loads(
                                tool_call.function.arguments
                            )
                        except (json.JSONDecodeError, TypeError):
                            arguments = {
                                "error": "Malformed JSON arguments"
                            }

                        result = None

                        for later_message in conversation[i + 1:]:
                            if (
                                isinstance(later_message, dict)
                                and later_message.get("role") == "tool"
                                and later_message.get("tool_call_id")
                                == tool_call.id
                            ):
                                try:
                                    result = json.loads(
                                        later_message.get("content", "{}")
                                    )
                                except json.JSONDecodeError:
                                    result = later_message.get("content")

                                break

                        st.session_state.tool_log.append({
                            "name": tool_call.function.name,
                            "arguments": arguments,
                            "result": result,
                        })

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
            })

            st.session_state.pending_messages = None

            st.rerun()

    with col2:
        if st.button("No, cancel"):

            answer = "Okay, I did not make the booking."

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
            })

            st.session_state.pending_messages = None

            st.rerun()
