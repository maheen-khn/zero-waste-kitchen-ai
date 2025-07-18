import streamlit as st
import json
import os

# Load recipes data
with open('recipes_with_filters.json', 'r', encoding='utf-8') as file:
    recipes = json.load(file)

# Set app page config
st.set_page_config(page_title="Zero-Waste Kitchen AI", layout="wide")

# --- Dark/Light Mode Toggle ---
dark_mode = st.sidebar.toggle("🌙 Dark Mode")
if dark_mode:
    st.markdown("""
        <style>
            body { background-color: #222; color: white; }
            .stButton button { color: black; background-color: white; }
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            body { background-color: #f5f5f5; color: black; }
        </style>
        """, unsafe_allow_html=True)

# --- Favorite Recipes Storage ---
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# --- Sidebar Filters ---
st.sidebar.title("🔍 Filter Your Recipes")

ingredient_filter = st.sidebar.text_input("Ingredient (any)")
cuisine_filter = st.sidebar.selectbox("Cuisine", ["All"] + sorted(list(set(r["cuisine"] for r in recipes))))
meal_type_filter = st.sidebar.selectbox("Meal Type", ["All"] + sorted(list(set(r["meal_type"] for r in recipes))))

# --- Filtering Logic ---
filtered_recipes = []
for recipe in recipes:
    if ingredient_filter.lower() not in ', '.join(recipe["ingredients"]).lower():
        continue
    if cuisine_filter != "All" and recipe["cuisine"] != cuisine_filter:
        continue
    if meal_type_filter != "All" and recipe["meal_type"] != meal_type_filter:
        continue
    filtered_recipes.append(recipe)

# --- Display Recipes ---
st.title("🥘 Zero-Waste Kitchen AI")
st.subheader("Find the best recipes based on your leftovers!")

cols = st.columns(3)

if filtered_recipes:
    for idx, recipe in enumerate(filtered_recipes):
        with cols[idx % 3]:
            st.image(recipe["image"], width=250)
            st.markdown(f"### {recipe['name']}")
            st.markdown(f"**Cuisine:** {recipe['cuisine']}  |  **Meal:** {recipe['meal_type']}")
            st.markdown(f"**Ingredients:** {', '.join(recipe['ingredients'])}")
            st.markdown("**Steps:**")
            for step in recipe["steps"]:
                st.markdown(f"- {step}")
            st.markdown(f"[▶ Watch on YouTube]({recipe['youtube']})")
            if st.button(f"💾 Save to Favorites", key=recipe["name"]):
                st.session_state.favorites.append(recipe)
                st.success(f"{recipe['name']} saved to favorites!")
else:
    st.warning("No recipes found matching your filters.")

# --- Show Favorites Section ---
if st.sidebar.button("💖 Show Favorites"):
    st.sidebar.markdown("### Your Favorite Recipes:")
    if st.session_state.favorites:
        for fav in st.session_state.favorites:
            st.sidebar.markdown(f"- {fav['name']}")
    else:
        st.sidebar.markdown("*No favorites saved yet.*")

