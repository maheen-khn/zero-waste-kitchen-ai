import streamlit as st
import json
import os
from PIL import Image
import requests
from io import BytesIO

# Load Recipes
with open("recipes_with_filters.json", "r") as f:
    recipes = json.load(f)

# Set page config and custom CSS for multicolor background
st.set_page_config(page_title="Zero-Waste Kitchen AI", layout="wide")

page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #FFE5EC, #E0BBE4, #957DAD, #D291BC, #FEC8D8);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
}
@keyframes gradient {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.recipe-card {
    background-color: #ffffffdd;
    border-radius: 20px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title
st.title("🍽️ Zero-Waste Kitchen AI")

# Tabs
tab1, tab2, tab3 = st.tabs(["🥘 Recipes", "🧂 Ingredients", "📷 Upload"])

# ------------------------ TAB 1 ------------------------
with tab1:
    st.header("Browse Recipes")

    # Filter controls
    cuisine_filter = st.selectbox("Filter by Cuisine", ["All"] + sorted(set(r["cuisine"] for r in recipes.values())))
    meal_filter = st.selectbox("Filter by Meal Type", ["All"] + sorted(set(r["meal_type"] for r in recipes.values())))

    # Display recipes
    for name, recipe in recipes.items():
        if (cuisine_filter == "All" or recipe["cuisine"] == cuisine_filter) and \
           (meal_filter == "All" or recipe["meal_type"] == meal_filter):
            with st.container():
                st.markdown(f"<div class='recipe-card'><h3>{name}</h3>", unsafe_allow_html=True)
                st.image(recipe["image"], width=300)
                st.markdown("**Ingredients:**")
                st.markdown(", ".join(recipe["ingredients"]))
                st.markdown("**Steps:**")
                for i, step in enumerate(recipe["steps"], 1):
                    st.markdown(f"{i}. {step}")
                if recipe["video"]:
                    st.video(recipe["video"])
                st.markdown("</div>", unsafe_allow_html=True)

# ------------------------ TAB 2 ------------------------
with tab2:
    st.header("Filter by Ingredients")
    input_ingredients = st.text_input("Enter ingredients (comma-separated)", "")
    if input_ingredients:
        input_set = set(i.strip().lower() for i in input_ingredients.split(","))
        matched = []
        for name, recipe in recipes.items():
            recipe_ingredients = set(i.lower() for i in recipe["ingredients"])
            if input_set & recipe_ingredients:
                matched.append((name, len(input_set & recipe_ingredients)))
        if matched:
            matched.sort(key=lambda x: x[1], reverse=True)
            for name, score in matched:
                st.subheader(name)
                st.markdown(f"Matched {score} ingredients.")
        else:
            st.warning("No matching recipes found.")

# ------------------------ TAB 3 ------------------------
with tab3:
    st.header("Upload Ingredient Image (OCR disabled for web version)")
    st.info("This feature is not available in the online version.")
