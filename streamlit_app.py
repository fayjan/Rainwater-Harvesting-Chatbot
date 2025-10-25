# streamlit_app.py

import streamlit as st
from app import build_qa_chain, cost_savings

st.set_page_config(page_title="💧 Rainwater Harvesting Chatbot", layout="wide")



# Title and description
st.title("💧 Rainwater Harvesting Assistant")
st.markdown("Learn how to **harvest rainwater**, **reduce costs**, and **implement sustainable systems** in your area.")

# Initialize chatbot
@st.cache_resource
def load_chain():
    return build_qa_chain()

qa_chain = load_chain()

# Chat UI
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I can help you with Rainwater Harvesting. What would you like to know?"}
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me about rainwater harvesting..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = qa_chain.run(prompt)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

st.subheader("💧 Rainwater Harvesting Assistant")

# Button to open calculator
if st.button("💰 Open Cost Saving Calculator"):
    with st.expander("Rainwater Cost Saving Calculator", expanded=True):
        st.markdown("### 🌦️ Estimate Your Annual Water Savings")

        area = st.number_input("🏠 Enter rooftop area (sq. ft):", min_value=0.0)
        rainfall = st.number_input("🌧️ Enter annual rainfall (mm):", min_value=0.0)
        cost = st.number_input("💸 Cost per litre (₹):", min_value=0.0, value=0.002, step=0.001)

        if st.button("Calculate Savings"):
            result = cost_savings(area, rainfall, cost)
            st.success(f"💰 Estimated Annual Savings: ₹{result:.2f}")
# End of streamlit_app.py