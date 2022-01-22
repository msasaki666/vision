import numpy as np
import pandas as pd
import requests
import streamlit as st

current_page_select = st.sidebar.radio(
    label="pages", options=["top", "df", "line", "area", "json"]
)
df = pd.DataFrame(np.random.randn(50, 20), columns=(i for i in range(1, 21)))

if current_page_select == "top":
    st.title("title")
    st.write("This is some text.")
    st.text("This is some text.")
if current_page_select == "df":
    st.dataframe(df.style.highlight_max())
if current_page_select == "line":
    st.line_chart(df)
if current_page_select == "area":
    st.area_chart(df)
if current_page_select == "json":
    if "apenapijson" not in st.session_state:
        res = requests.get("https://petstore.swagger.io/v2/swagger.json")
        st.session_state["apenapijson"] = res.json()
    st.json(st.session_state.apenapijson)
