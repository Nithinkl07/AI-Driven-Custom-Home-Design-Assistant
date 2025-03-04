import streamlit as st
import google.generativeai as genai
import requests

# Configure API Keys (Replace with your actual keys)
GOOGLE_API_KEY = "AIzaSyDiakHkuvwpay0EFSeQwL_Hbfmp1t81LF0"
PEXELS_API_KEY = "hOH6iml510Jij0iI6UUxohxJGh6R6Ml4BmBUHmdg19FovYOJVvz8gGY3"

# Configure Google Generative AI
genai.configure(api_key=GOOGLE_API_KEY)

# Function to generate home design ideas using AI
def generate_design_idea(style, size, rooms):
    model = genai.GenerativeModel("gemini-1.5-pro")

    prompt = f"""
    Create a home design plan with:
    - Style: {style}
    - Size: {size} sq ft
    - Number of rooms: {rooms}

    Include layout suggestions, color schemes, and furniture recommendations.
    """

    response = model.generate_content(prompt)
    return response.text if response.text else "No response generated."

# Function to fetch an image from Pexels API
def fetch_image_from_pexels(query):
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 1}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data["photos"]:
                return data["photos"][0]["src"]["large"]
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None

# Streamlit UI
st.title("🏡 Custom Home Design Assistant")

# User input fields
style = st.text_input("🏠 Enter Home Design Style (e.g., Modern, Rustic)")
size = st.text_input("📏 Enter Home Size (sq ft)")
rooms = st.text_input("🛏️ Enter Number of Rooms")

# Generate Design Button
if st.button("🔍 Generate Design"):
    if style and size and rooms:
        with st.spinner("Generating Home Design... ⏳"):
            # Generate design idea using AI
            design_idea = generate_design_idea(style, size, rooms)

            # Fetch images for different categories
            interior_image = fetch_image_from_pexels(f"{style} interior design")
            exterior_image = fetch_image_from_pexels(f"{style} house exterior")
            architecture_image = fetch_image_from_pexels(f"{style} house architecture")

        # Display AI-generated home design idea
        st.subheader("🏡 AI-Generated Home Design Plan")
        st.markdown(design_idea)

        # Display images in sections
        st.subheader("📸 Suggested Home Design Images")

        col1, col2, col3 = st.columns(3)
        
        if interior_image:
            col1.image(interior_image, use_container_width=True, caption="Interior Design")
        else:
            col1.warning("No interior image found.")

        if exterior_image:
            col2.image(exterior_image, use_container_width=True, caption="Exterior View")
        else:
            col2.warning("No exterior image found.")

        if architecture_image:
            col3.image(architecture_image, use_container_width=True, caption="Architectural Design")
        else:
            col3.warning("No architectural image found.")
        
    else:
        st.warning("⚠️ Please enter all details.")
