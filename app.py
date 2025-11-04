# ----------------
# Working Code
# # ----------------
import streamlit as st
import os
import pdfkit

# -----------------------------
# ✅ wkhtmltopdf Configuration
# -----------------------------
# ⚠️ Update this path to where wkhtmltopdf.exe is located on your system
# Example: C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe
path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# -----------------------------
# Streamlit UI Setup
# -----------------------------
st.set_page_config(page_title="Web & PDF Converter", page_icon="📄", layout="centered")
st.title("📄 Web & PDF Converter App")
st.write("Convert any **webpage** or **uploaded PDF** and store it neatly in your `repo` folder.")

# -----------------------------
# Folder Setup
# -----------------------------
BASE_REPO = "folder_base"
if not os.path.exists(BASE_REPO):
    os.makedirs(BASE_REPO)

st.subheader("📁 Folder Management")
folder_name = st.text_input("Enter folder name (optional):")

if st.button("Create Folder"):
    folder_path = os.path.join(BASE_REPO, folder_name) if folder_name else BASE_REPO
    os.makedirs(folder_path, exist_ok=True)
    st.success(f"Folder created or verified: `{folder_path}`")

# Final folder path for saving files
folder_path = os.path.join(BASE_REPO, folder_name) if folder_name else BASE_REPO

# -----------------------------
# Option Selection
# -----------------------------
st.subheader("Choose an Option")
option = st.radio("Select Input Type:", ("Web", "PDF"))

# -----------------------------
# Option 1: Web Scraping (via wkhtmltopdf)
# -----------------------------
if option == "Web":
    st.write("Convert a website directly into a PDF.")
    url = st.text_input("Enter the website URL:")

    if st.button("Scrape & Convert to PDF"):
        if not url:
            st.error("Please enter a valid URL.")
        else:
            try:
                pdf_name = "webpage_output.pdf"
                pdf_path = os.path.join(folder_path, pdf_name)
                os.makedirs(folder_path, exist_ok=True)

                # ✅ Generate the PDF using pdfkit (renders full webpage)
                pdfkit.from_url(url, pdf_path, configuration=config)

                st.success(f"✅ PDF saved successfully at: `{pdf_path}`")

                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=f,
                        file_name=pdf_name,
                        mime="application/pdf"
                    )

            except Exception as e:
                st.error(f"⚠️ Error: {e}")

# -----------------------------
# Option 2: PDF Upload
# -----------------------------
elif option == "PDF":
    st.write("📄 Upload an existing PDF file.")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        pdf_path = os.path.join(folder_path, uploaded_file.name)
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ PDF saved successfully at: `{pdf_path}`")

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Uploaded PDF",
                data=f,
                file_name=uploaded_file.name,
                mime="application/pdf"
            )

# -----------------------------
# Display Folder Contents
# -----------------------------
st.subheader("📂 Folder Contents")
if os.path.exists(folder_path):
    files = os.listdir(folder_path)
    if files:
        for file in files:
            st.write(f"- {file}")
    else:
        st.info("This folder is currently empty.")
