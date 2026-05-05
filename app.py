import os
import streamlit as st
from dotenv import load_dotenv
from tools.generate_content import generate_page

load_dotenv()

st.set_page_config(page_title="viAct Industry Page & SEO Generator", layout="wide")
st.title("viAct Industry Page & SEO Generator")

industry_name = st.text_input("Industry Name", placeholder="e.g. Mining, Logistics, Oil & Gas")

if st.button("Generate Page", type="primary"):
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except (KeyError, FileNotFoundError):
            pass

    if not api_key:
        st.error("GEMINI_API_KEY not found. Add it to your .env file or Streamlit secrets.")
    elif not industry_name.strip():
        st.warning("Please enter an industry name.")
    else:
        with st.spinner(f"Generating industry page for **{industry_name}**..."):
            try:
                result = generate_page(industry_name.strip(), api_key)
                st.success("Page generated successfully!")

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Rendered Preview")
                    st.markdown(result)
                with col2:
                    st.subheader("Raw Markdown (Copy)")
                    st.code(result, language="markdown")
            except Exception as e:
                st.error(f"Generation failed: {e}")
