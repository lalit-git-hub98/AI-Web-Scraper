import streamlit as st
# from scrape import (
#     scrape_website,
#     extract_body_content,
#     clean_body_content,
#     split_dom_content,
# )
from scrape import *
from parse import parse_with_openai

# Streamlit UI
st.markdown("<h1 style='text-align: center;'>🤖 ScraperBot 🌐</h1>", unsafe_allow_html=True)
url = st.text_input("Enter Website URL")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if url:
        st.write("Scraping the website...")

        # Scrape the website
        dom_content = scrape_website(url)
        st.success("Success")
        body_content = extract_body_content(dom_content)
        cleaned_content = clean_body_content(body_content)

        # Store the DOM content in Streamlit session state
        st.session_state.dom_content = cleaned_content

        # Display the DOM content in an expandable text box
        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)


# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    parse_description = st.text_area("Tell me what information you want from the website")

    if st.button("Get Information"):
        if parse_description:
            st.write("Generating Answer...")

            # Parse the content with Ollama
            dom_chunks = split_dom_content(st.session_state.dom_content)
            st.write(dom_chunks)
            parsed_result = parse_with_openai(dom_chunks, parse_description)
            st.write(parsed_result)