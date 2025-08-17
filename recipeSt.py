import random
import streamlit as st
from collections import defaultdict
import pandas as pd
import io
import base64
from datetime import datetime
from github import Github

# ==== Recipe Catalog ====
recipeDinner = {
    "Burrito": ["Refried Beans", "Tortillas", "Mexican Cheese", "Rice"],
    "Tilapia": ["Tilapia", "Green Beans", "Couscous"],
    "Chickpea Curry": ["Chickpeas", "Rice", "Curry Sauce"],
    "Grilled Cheese": ["Bread", "American Cheese", "Tomato Soup"],
    "Cauliflower Skillet": ["Cauliflower", "Mushrooms", "Tofu"],
    "Sausage Skillet": ["White Beans", "White Beans", "Smoked Sausage", "Spinach"],
    "Fried Rice": ["Rice", "Veggies", "Tofu"],
    "Vodka Pasta": ["Tomato Paste", "Heavy Cream"],
    "Egg Roll Bowl": ["Sausage", "Cole Slaw", "Rice"],
    "Croissant Dogs": ["Hot Dogs", "Croissants"],
    "Fiesta Lime Chicken": ["Chicken", "Mexican Cheese", "Salsa", "Ranch", "Mexican Rice"],
    "Chicken Tacos": ["Chicken", "Mexican Cheese", "Corn Tortillas"],
    "Chicken Parm": ["Red Bag Chicken", "Tomato Sauce", "Italian Cheese"],
    "Rice Bowl": ["Chicken", "Edamame", "Rice", "Asian Sauce"],
    "Pierogis and Brussels": ["Pierogis", "Brussel Sprouts"],
    "Ramen": ["Ramen"]
}

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def grocer(plan):
    grocList = []
    for x in plan.values():
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


def update_github_file_append_with_timestamp(repo_name, file_path, new_plan_df, commit_message):
    token = st.secrets["GITHUB_TOKEN"]
    g = Github(token)
    repo = g.get_repo(repo_name)

    # Add timestamp column to new data
    new_plan_df["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        file = repo.get_contents(file_path)
        existing_content = base64.b64decode(file.content).decode("utf-8")
        existing_df = pd.read_csv(io.StringIO(existing_content))
        combined_df = pd.concat([existing_df, new_plan_df], ignore_index=True)
        combined_df.drop_duplicates(inplace=True)
        csv_buffer = io.StringIO()
        combined_df.to_csv(csv_buffer, index=False)
        updated_content = csv_buffer.getvalue()
        repo.update_file(file.path, commit_message, updated_content, file.sha)
    except Exception:
        csv_buffer = io.StringIO()
        new_plan_df.to_csv(csv_buffer, index=False)
        repo.create_file(file_path, commit_message, csv_buffer.getvalue())


# --- Streamlit UI ---

st.title("Weekly Meal Planner")

menu_choice = st.sidebar.radio(
    "Choose an option:",
    ["View recipe book", "Randomly generate weekly plan", "Manually create weekly plan"]
)

# --- Option 1: View recipe book ---
if menu_choice == "View recipe book":
    st.subheader("Recipe Book")
    for recipe, ingredients in recipeDinner.items():
        with st.expander(recipe):
            st.write(", ".join(ingredients))

# --- Option 2: Randomly generate weekly plan ---
elif menu_choice == "Randomly generate weekly plan":
    if "randPlan" not in st.session_state:
        keys = list(recipeDinner.keys())
        random.shuffle(keys)
        st.session_state.randPlan = {days[i]: keys[i] for i in range(len(days))}

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Rerandomize"):
            keys = list(recipeDinner.keys())
            random.shuffle(keys)
            st.session_state.randPlan = {days[i]: keys[i] for i in range(len(days))}
    with col2:
        if st.button("Generate Grocery List"):
            grocery_list = grocer(st.session_state.randPlan)
            st.subheader("Grocery List")
            for item in grocery_list:
                st.write(item)
    with col3:
        if st.button("Append weekly plan CSV on GitHub"):
            try:
                plan_df = pd.DataFrame(list(st.session_state.randPlan.items()), columns=["Day", "Recipe"])
                update_github_file_append_with_timestamp(
                    "ZaneKelley12/grocery",
                    "weekly_meal_plan.csv",
                    plan_df,
                    "Append random weekly meal plan CSV with timestamp from Streamlit app"
                )
                st.success("GitHub file updated with appended data and timestamp!")
            except Exception as e:
                st.error(f"Error updating GitHub file: {e}")

    st.subheader("Weekly Plan")
    for day in days:
        st.session_state.randPlan[day] = st.selectbox(
            f"{day}:",
            list(recipeDinner.keys()),
            index=list(recipeDinner.keys()).index(st.session_state.randPlan[day]),
            key=f"rand_{day}"
        )

# --- Option 3: Manually create weekly plan ---
elif menu_choice == "Manually create weekly plan":
    if "manPlan" not in st.session_state:
        st.session_state.manPlan = {day: list(recipeDinner.keys())[0] for day in days}

    st.subheader("Select Recipes for Each Day")
    for day in days:
        st.session_state.manPlan[day] = st.selectbox(
            f"{day}:",
            list(recipeDinner.keys()),
            index=list(recipeDinner.keys()).index(st.session_state.manPlan[day]),
            key=f"man_{day}"
        )

    if st.button("Generate Grocery List"):
        grocery_list = grocer(st.session_state.manPlan)
        st.subheader("Grocery List")
        for item in grocery_list:
            st.write(item)

    if st.button("Append weekly plan CSV on GitHub"):
        try:
            plan_df = pd.DataFrame(list(st.session_state.manPlan.items()), columns=["Day", "Recipe"])
            update_github_file_append_with_timestamp(
                "ZaneKelley12/grocery",
                "weekly_meal_plan.csv",
                plan_df,
                "Append manual weekly meal plan CSV with timestamp from Streamlit app"
            )
            st.success("GitHub file updated with appended data and timestamp!")
        except Exception as e:
            st.error(f"Error updating GitHub file: {e}")
