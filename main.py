import streamlit as st
import json

# Load recipes from JSON file
with open("recipes_with_images.json", "r") as file:
    recipes = json.load(file)

# Streamlit page config
st.set_page_config(page_title="Zero-Waste Kitchen AI", layout="wide")
st.title("🍲 Zero-Waste Kitchen AI")

# Create two tabs only (no OCR)
tab2, tab3 = st.tabs(["🖊️ Manual Entry", "📜 All Recipes"])

# Matching function
def get_matching_recipes(input_ingredients):
    input_set = set(ingredient.lower() for ingredient in input_ingredients)
    matches = []
    for name, data in recipes.items():
        recipe_set = set(i.lower() for i in data["ingredients"])
        common = input_set.intersection(recipe_set)
        score = len(common)
        if score > 0:
            matches.append((name, score))
    matches.sort(key=lambda x: x[1], reverse=True)
    return [name for name, score in matches]

# Tab 2 – Manual Entry
with tab2:
    st.header("🖊️ Enter Ingredients Manually")
    input_text = st.text_area("List ingredients separated by commas", placeholder="e.g. onion, tomato, rice")
    
    if st.button("Get Recipes"):
        ingredients = [x.strip().lower() for x in input_text.split(",") if x.strip()]
        if ingredients:
            matched = get_matching_recipes(ingredients)
            st.subheader("🍽️ Suggested Recipes:")
            if matched:
                for name in matched:
                    data = recipes[name]
                    st.image(data["image"], width=300, caption=name)
                    st.markdown(f"**Ingredients:** {', '.join(data['ingredients'])}")
            else:
                st.warning("❌ No matching recipes found.")
        else:
            st.warning("Please enter at least one ingredient.")

# Tab 3 – All Recipes
with tab3:
    st.header("📜 All Available Recipes")
    for name, data in recipes.items():
        st.image(data["image"], width=300, caption=name)
        st.markdown(f"**Ingredients:** {', '.join(data['ingredients'])}")
        st.markdown("---")
