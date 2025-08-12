import random
import streamlit as st
from collections import defaultdict

# ==== Recipe Catalog ====
recipeDinner = {
    "Burrito": ["Refried Beans", "Tortillas", "Mexican Cheese", "Rice"],
    "Tilapia": ["Tilapia", "Green Beans", "Couscous"],
    "Chickpea Curry": ["Chickpeas", "Rice", "Curry Sauce"],
    "Grilled Cheese": ["Bread", "American Cheese", "Tomato Soup"],
    "Cauliflower Skillet": ["Cauliflower", "Mushrooms", "Tofu"],
    "Sausage Skillet": ["White Beans", "White Beans", "Smoked Sausage", "Spinach"],
    "Fried Rice": ["Rice", "Veggies"],
    "Vodka Pasta": ["Tomato Paste", "Heavy Cream"]
}

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# ==== Grocery List Function ====
def grocer(randPlan):
    grocList = []
    for x in randPlan.values():
        if x in recipeDinner:
            grocList.append(recipeDinner[x])

    flat = [item for sublist in grocList for item in sublist]

    counts = defaultdict(int)
    for item in flat:
        counts[item] += 1

    result = []
    blocklist = {"Bread", "Tortillas", "Rice"}

    for item in counts:
        if item in blocklist:
            result.append(item)
        else:
            count = counts[item]
            if count == 1:
                result.append(item)
            else:
                result.append(f"{count}x {item}")

    return sorted(result)

# ==== Streamlit UI ====
st.title("Weekly Meal Planner")
st.sidebar.header("Menu Options")

menu_choice = st.sidebar.radio(
    "Choose an option:",
    ["View recipe book", "Randomly generate weekly plan", "Manually create weekly plan"]
)

# --- Option 1: View Recipe Book ---
if menu_choice == "View recipe book":
    st.subheader("Recipe Book")
    for recipe, ingredients in recipeDinner.items():
        with st.expander(recipe):
            st.write(", ".join(ingredients))

# --- Option 2: Randomly Generate Plan ---
elif menu_choice == "Randomly generate weekly plan":
    if "randPlan" not in st.session_state:
        keys = list(recipeDinner.keys())
        random.shuffle(keys)
        st.session_state.randPlan = {days[i]: keys[i] for i in range(len(days))}

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Rerandomize"):
            keys = list(recipeDinner.keys())
            random.shuffle(keys)
            st.session_state.randPlan = {days[i]: keys[i] for i in range(len(days))}

    with col2:
        if st.button("Generate Grocery List"):
            st.subheader("Grocery List")
            for item in grocer(st.session_state.randPlan):
                st.write(item)

    st.subheader("Weekly Plan")
    for day in days:
        st.session_state.randPlan[day] = st.selectbox(
            f"{day}:",
            list(recipeDinner.keys()),
            index=list(recipeDinner.keys()).index(st.session_state.randPlan[day])
        )

# --- Option 3: Manually Create Plan ---
elif menu_choice == "Manually create weekly plan":
    if "manPlan" not in st.session_state:
        st.session_state.manPlan = {day: list(recipeDinner.keys())[0] for day in days}

    st.subheader("Select Recipes for Each Day")
    for day in days:
        st.session_state.manPlan[day] = st.selectbox(
            f"{day}:",
            list(recipeDinner.keys()),
            index=list(recipeDinner.keys()).index(st.session_state.manPlan[day])
        )

    if st.button("Generate Grocery List"):
        st.subheader("Grocery List")
        for item in grocer(st.session_state.manPlan):
            st.write(item)
