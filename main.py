import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama

# Streamlit UI
st.set_page_config(page_title="AI Web Scraper", layout="wide")
st.title("🔍 AI-Powered Web Scraper")

# Step 1: User Input for Website URL
url = st.text_input("🌐 Enter Website URL", placeholder="https://example.com")

if st.button("🚀 Scrape Website"):
    if url:
        st.write("🔄 Scraping the website... Please wait.")

        # Scrape the website
        dom_content = scrape_website(url)

        if dom_content:
            body_content = extract_body_content(dom_content)
            cleaned_content = clean_body_content(body_content)

            # Store the cleaned content in Streamlit session state
            st.session_state.dom_content = cleaned_content

            # Display the DOM content in an expandable section
            with st.expander("📜 View Extracted Website Content"):
                st.text_area("DOM Content", cleaned_content, height=300)
        else:
            st.error("❌ Failed to scrape the website. Please check the URL or try again.")

# Step 2: User Input for Parsing Instructions
if "dom_content" in st.session_state:
    parse_description = st.text_area(
        "✏️ Describe what you want to extract",
        placeholder="Describe the information you want to extract from the page ",
    )

    if st.button("🔎 Parse Content"):
        if parse_description:
            st.write("🧠 AI is extracting relevant information...")

            # Split large DOM content into chunks
            dom_chunks = split_dom_content(st.session_state.dom_content)

            # Pass content to AI model for processing
            parsed_result = parse_with_ollama(dom_chunks, parse_description).strip()

            # Display cleaned result
            if parsed_result:
                st.success("✅ Extraction Successful!")
                st.write(parsed_result)
            else:                     
                st.warning("⚠️ No matching content found.")
