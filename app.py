import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(
    page_title="Text-to-SQL Analytics Agent",
    page_icon="🤖",
    layout="wide"
)

API_URL = "http://localhost:8000"

st.title("🤖 Self-Correcting Text-to-SQL Analytics Agent")
st.markdown("""
Ask business analytics questions in natural language. The stateful agent plans, generates validated SQL, requests human approval, executes against the e-commerce database, self-corrects on errors, and visualizes insights.
""")

# Sidebar
st.sidebar.header("Database Schema & Info")
try:
    schema_res = requests.get(f"{API_URL}/schema", timeout=3)
    if schema_res.status_code == 200:
        schema = schema_res.json()
        for table, cols in schema.items():
            with st.sidebar.expander(f"Table: {table}"):
                st.write(", ".join(cols))
    else:
        st.sidebar.warning("Could not fetch schema from API. Ensure FastAPI is running.")
except Exception:
    st.sidebar.info("FastAPI backend not detected at localhost:8000. Start it with `uvicorn main:app --reload`.")

st.sidebar.markdown("---")
st.sidebar.markdown("### Example Prompts")
examples = [
    "What are the top 5 products by revenue?",
    "Show customer count by country",
    "What is the breakdown of order statuses?",
    "Show supplier details and product count",
    "What is the average price by product category?"
]
selected_example = st.sidebar.selectbox("Choose an example", [""] + examples)

# Main query input
query_input = st.text_input("Enter your analytics question:", value=selected_example if selected_example else "")

col1, col2 = st.columns([1, 5])
with col1:
    submit_btn = st.button("Run Analysis", type="primary")

if submit_btn and query_input:
    with st.spinner("Agent is planning, generating SQL, validating, and executing..."):
        try:
            payload = {"query": query_input, "auto_approve": True}
            res = requests.post(f"{API_URL}/query", json=payload, timeout=10)
            if res.status_code == 200:
                data = res.json()

                # Display Agent Steps
                st.subheader("Agent Workflow & Reasoning")
                tab1, tab2, tab3, tab4 = st.tabs(["Plan", "Generated SQL", "Validation", "Execution & Summary"])

                with tab1:
                    st.info(data["plan"])
                with tab2:
                    st.code(data["sql_query"], language="sql")
                with tab3:
                    if data["validation_result"]:
                        st.success(data["validation_message"])
                    else:
                        st.error(data["validation_message"])
                with tab4:
                    st.write(f"**Execution Success:** {data['execution_success']}")
                    st.write(f"**Retries Used:** {data['retry_count']}")
                    st.write(f"**Summary:** {data['summary']}")
                    if data["error_message"]:
                        st.error(f"Error: {data['error_message']}")

                # Display Results Table & Chart
                st.subheader("Results")
                if data["results"] and data["columns"]:
                    df = pd.DataFrame(data["results"], columns=data["columns"])
                    st.dataframe(df, use_container_width=True)

                    # Simple chart visualization if numerical data exists
                    if len(df.columns) >= 2 and pd.api.types.is_numeric_dtype(df[df.columns[1]]):
                        st.subheader("Data Visualization")
                        st.bar_chart(df.set_index(df.columns[0])[df.columns[1]])
                else:
                    st.info("No data returned for this query.")

            else:
                st.error(f"API Error: {res.text}")
        except Exception as e:
            st.error(f"Failed to connect to FastAPI backend: {e}")
elif submit_btn:
    st.warning("Please enter a query.")
