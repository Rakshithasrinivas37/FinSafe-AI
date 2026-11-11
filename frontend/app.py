
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/api/v1/analyse/message"

st.set_page_config(
    page_title="FinSafe AI",
    page_icon="🛡️",
    layout="centered",
)

st.title("🛡️ FinSafe AI")
st.subheader("Your Personal Financial Safety Assistant")

st.write(
    "Analyse suspicious messages and understand "
    "potential financial-safety risks."
)

st.info(
    "Prototype: Do not enter real OTPs, passwords, "
    "PINs, card numbers or banking credentials. "
    "Use sample messages until privacy protections "
    "are implemented."
)

message = st.text_area(
    "Enter the message you want to analyse",
    placeholder=(
        "Example: Your bank account will be blocked. "
        "Verify your account immediately."
    ),
    height=180,
)

jurisdiction = st.selectbox(
    "Select your jurisdiction",
    ["Singapore", "India", "Indonesia", "Other"],
)

if st.button("Analyse Message", type="primary"):

    if not message.strip():
        st.warning("Please enter a message.")

    else:
        try:
            with st.spinner("Submitting your message..."):
                response = requests.post(
                    API_URL,
                    json={
                        "message": message,
                        "jurisdiction": jurisdiction,
                    },
                    timeout=15,
                )

            if response.status_code == 200:
                result = response.json()

                st.divider()
                st.header("Analysis Result")

                # Display API status
                status = result.get("status", "unknown")

                if status == "completed":
                    st.success("Analysis completed successfully!")
                elif status == "pending_implementation":
                    st.info("Message received. Scam detection is not implemented yet.")
                else:
                    st.warning(f"Analysis status: {status}")

                # Display API message
                st.subheader("Message")
                st.write(result.get("message", "No message returned."))

                # Display analysis
                st.subheader("Analysis")
                st.write(result.get("analysis", "No analysis available."))

            else:
                st.error(
                    f"API error: {response.status_code}"
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "Unable to connect to the backend. "
                "Please start the FastAPI server."
            )

        except requests.exceptions.Timeout:
            st.error("The backend request timed out.")
