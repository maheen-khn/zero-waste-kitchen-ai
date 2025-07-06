import streamlit as st
import json

# Load recipe data
with open("recipes_with_images.json", "r") as f:
    recipes = json.load(f)

# Custom multicolor background CSS
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%);
        font-family: 'Segoe UI', sans-serif;
    }
    .stApp {
        background: linear-gradient(to right, #fceabb, #f8b500, #fceabb);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        padding: 2rem;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .recipe-card {
        background-color: #ffffffcc;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🍽️ Zero-Waste Kitchen AI")
st.write("Reduce food waste by discovering recipes based on your available ingredients.")

# Filter section
st.subheader("🔍 Find recipes by ingredient")
ingredient_query = st.text_input("Enter an ingredient (e.g., rice, paneer, pasta):").strip().lower()

# Recipe display
found = False
for name, data in recipes.items():
    if ingredient_query in " ".join(data["ingredients"]).lower() or ingredient_query == "":
        found = True
        with st.container():
            st.markdown(f"### 🍛 {name}")
            st.image(data["image"], use_column_width=True)
            st.markdown("**📝 Ingredients:**")
            st.markdown(", ".join(data["ingredients"]))
            st.markdown("**👩‍🍳 Steps:**")
            for step in data["steps"]:
                st.markdown(f"- {step}")
            st.markdown("**🎥 Watch Tutorial:**")
            st.video(data["video"])
            st.markdown("---")

if not found and ingredient_query:
    st.warning("No matching recipes found. Try a different ingredient.")
