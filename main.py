import streamlit as st
import json

# Set page config
st.set_page_config(page_title="Zero-Waste Kitchen AI", layout="wide")

# Custom pastel multi-color background
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to bottom right, #fceabb, #f8b500, #ffecd2, #fcb69f, #a1c4fd, #c2e9fb);
        background-size: 600% 600%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    h1, h2, h3 {
        color: #4CAF50;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load data
with open("recipes_with_images.json", "r") as file:
    recipes = json.load(file)

st.title("🍲 Zero-Waste Kitchen AI")

# Matching logic
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

# Create tabs
tab2, tab3 = st.tabs(["🖊️ Enter Ingredients", "📜 All Recipes"])

# Tab 2: Manual entry
with tab2:
    st.header("🖊️ Enter Ingredients You Have")
    input_text = st.text_area("List ingredients separated by commas", placeholder="e.g. onion, tomato, rice")
    
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
                    st.markdown(f"**🥗 Ingredients:** {', '.join(data['ingredients'])}")
                    
                    if "steps" in data:
                        st.markdown("**👣 Steps to Prepare:**")
                        for i, step in enumerate(data["steps"], 1):
                            st.markdown(f"{i}. {step}")
                    
                    if "video" in data and data["video"]:
                        st.markdown("**🎥 Watch Tutorial:**")
                        st.video(data["video"])
                    
                    st.markdown("---")
        else:
            st.warning("❌ No matching recipes found.")
    else:
        st.info("Please enter ingredients to get suggestions.")

# Tab 3: All Recipes
with tab3:
    st.header("📜 All Recipes in the System")
    for name, data in recipes.items():
        st.image(data["image"], width=300, caption=name)
        st.markdown(f"**🥗 Ingredients:** {', '.join(data['ingredients'])}")

        if "steps" in data:
            st.markdown("**👣 Steps to Prepare:**")
            for i, step in enumerate(data["steps"], 1):
                st.markdown(f"{i}. {step}")

        if "video" in data and data["video"]:
            st.markdown("**🎥 Watch Tutorial:**")
            st.video(data["video"])

        st.markdown("---")


