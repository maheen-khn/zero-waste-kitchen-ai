import streamlit as st
import json

# Page config and style
st.set_page_config(page_title="Zero-Waste Kitchen AI", layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background-color: #fffaf0;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3 {
        color: #4CAF50;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🍲 Zero-Waste Kitchen AI")

# Load recipes
with open("recipes_with_images.json", "r") as file:
    recipes = json.load(file)

# Create tabs (no OCR)
tab2, tab3 = st.tabs(["🖊️ Enter Ingredients", "📜 All Recipes"])

# Helper function for matching
def get_matching_recipes(input_ingredients):
    input_set = set(i.lower() for i in input_ingredients)
    matches = []
    for name, data in recipes.items():
        recipe_set = set(i.lower() for i in data["ingredients"])
        score = len(input_set.intersection(recipe_set))
        if score > 0:
            matches.append((name, score))
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches

# Tab 2 – Manual Entry + Filters
with tab2:
    st.header("🖊️ Enter Ingredients You Have")
    input_text = st.text_area("Enter ingredients separated by commas:", placeholder="e.g. rice, onion, tomato")
    
    if input_text.strip():
        ingredients = [i.strip().lower() for i in input_text.split(",") if i.strip()]
        matches = get_matching_recipes(ingredients)

        with st.expander("🔍 Filters & Sorting", expanded=False):
            min_match = st.slider("Minimum matching ingredients", 1, 10, 1)
            sort_alpha = st.checkbox("Sort results alphabetically (A–Z)")

        st.subheader("🍽️ Suggested Recipes")
        if matches:
            if sort_alpha:
                matches.sort(key=lambda x: x[0])
            for name, score in matches:
                if score >= min_match:
                    data = recipes[name]
                    st.image(data["image"], width=300, caption=name)
                    st.markdown(f"**Ingredients:** {', '.join(data['ingredients'])}")
                    st.markdown("---")
        else:
            st.warning("❌ No matching recipes found.")
    else:
        st.info("Please enter ingredients to get suggestions.")

# Tab 3 – All Recipes
with tab3:
    st.header("📜 All Recipes in the System")
    for name, data in recipes.items():
        st.image(data["image"], width=300, caption=name)
        st.markdown(f"**Ingredients:** {', '.join(data['ingredients'])}")
        st.markdown("---")


