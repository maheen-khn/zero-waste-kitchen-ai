import streamlit as st
import json
import random
import requests

# Load recipes data
def load_recipes():
    with open("recipes_with_filters.json", "r") as f:
        return json.load(f)

def filter_recipes(recipes, ingredients, cuisine_filter, meal_filter):
    filtered = []
    for name, data in recipes.items():
        if cuisine_filter != "All" and data.get("cuisine") != cuisine_filter:
            continue
        if meal_filter != "All" and data.get("meal_type") != meal_filter:
            continue
        if all(ing.lower() in [i.lower() for i in data["ingredients"]] for ing in ingredients):
            filtered.append((name, data))
    return filtered

def get_recipe_display(name, data):
    st.subheader(name)
    st.image(data["image"], use_column_width=True)
    st.markdown(f"**Cuisine:** {data['cuisine']}  |  **Meal:** {data['meal_type']}")
    st.markdown("**Ingredients:**")
    st.write(", ".join(data["ingredients"]))
    st.markdown("**Steps:**")
    for step in data["steps"]:
        st.write(f"- {step}")
    if data.get("video"):
        st.video(data["video"])
    if st.button(f"❤️ Save {name}", key=name):
        st.session_state.favorites.add(name)

# UI Configuration
st.set_page_config(page_title="Zero-Waste Kitchen AI", layout="wide")
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #ffe6f0, #e6f7ff, #e6ffe6);
        }
        .stApp {
            background-color: transparent;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🥗 Zero-Waste Kitchen AI")
recipes = load_recipes()

if "favorites" not in st.session_state:
    st.session_state.favorites = set()

# Input Section
with st.sidebar:
    st.header("Filter Recipes")
    ingredient_input = st.text_input("Enter ingredients (comma separated):")
    cuisine_filter = st.selectbox("Cuisine Type", ["All"] + sorted(set(r["cuisine"] for r in recipes.values())))
    meal_filter = st.selectbox("Meal Type", ["All"] + sorted(set(r["meal_type"] for r in recipes.values())))
    search = st.button("Search Recipes")
    st.markdown("---")
    if st.session_state.favorites:
        st.write("**❤️ Saved Recipes:**")
        for fav in st.session_state.favorites:
            st.write(f"- {fav}")

if search:
    ingredients = [i.strip() for i in ingredient_input.split(",") if i.strip()]
    matches = filter_recipes(recipes, ingredients, cuisine_filter, meal_filter)
    if matches:
        for name, data in matches:
            get_recipe_display(name, data)
    else:
        st.warning("No matching recipes found. Try different filters or ingredients.")
else:
    st.info("Enter ingredients and click 'Search Recipes' to begin.")
