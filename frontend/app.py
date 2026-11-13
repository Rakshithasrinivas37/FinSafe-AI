
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
            with st.spinner("Analysing your message..."):
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

                # 1. API status
                status = result.get("status", "unknown")

                if status == "completed":
                    st.success("Analysis completed successfully!")
                else:
                    st.warning(f"Analysis status: {status}")

                # 2. Risk assessment
                risk_assessment = result.get(
                    "risk_assessment", {}
                )

                risk_level = risk_assessment.get(
                    "risk_level", "unknown"
                ).lower()

                st.subheader("Risk Assessment")

                if risk_level == "high":
                    st.error("🔴 HIGH RISK")
                elif risk_level == "medium":
                    st.warning("🟠 MEDIUM RISK")
                elif risk_level == "low":
                    st.success("🟢 LOW RISK")
                else:
                    st.info("Risk level unavailable.")

                # 2.1 AI-generated analysis
                st.subheader("AI-Powered Analysis")

                analysis = result.get("analysis", "")

                if analysis:
                    st.markdown(analysis)
                else:
                    st.info("AI-generated explanation is unavailable.")

                # 2.2 Deterministic risk explanation
                st.subheader("Rule-Based Risk Assessment")

                st.write(
                    risk_assessment.get(
                        "explanation",
                        "No risk explanation available.",
                    )
                )

                # 3. Detected indicators
                st.subheader("Detected Indicators")

                indicators = result.get("indicators", [])

                if indicators:
                    for indicator in indicators:
                        category = (
                            indicator["category"]
                            .replace("_", " ")
                            .title()
                        )

                        matched_text = indicator["matched_text"]

                        st.warning(
                            f"**{category}**: "
                            f'"{matched_text}"'
                        )
                else:
                    st.info("No known risk indicators detected.")

                # 4. Risk reasons
                st.subheader("Why was this risk level assigned?")

                reasons = risk_assessment.get("reasons", [])

                if reasons:
                    for reason in reasons:
                        st.markdown(f"- {reason}")
                else:
                    st.write("No specific reasons available.")

                # 5. Safety disclaimer
                st.divider()

                st.caption(
                    "Important: This is an automated preliminary "
                    "assessment, not a definitive fraud verdict. "
                    "A low-risk result does not guarantee that "
                    "a message is legitimate. Verify requests "
                    "through official channels."
                )

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

        except requests.exceptions.RequestException:
            st.error("An unexpected network error occurred.")

        except ValueError:
            st.error("The backend returned an invalid response.")
