import streamlit as st
from code_editor import code_editor

st.title("Reinforcement Learning Trail")

st.subheader("Tooltips usage example", help="Select a code snippet to see its tooltip.")

def interactive_code_with_tooltips(code: str, tooltips: dict):
    editor_btns = [{
        "name": "Learn",
        "feather": "Bell",
        "primary": True,
        "hasText": True,
        "showWithIcon": True,
        "alwaysOn": True,
        "commands": ["submit"],
        "style": {"top": "-0.25rem", "right": "0.4rem"}
    }]
    result = code_editor(code, lang="python", theme="default", height=[5, 17], buttons=editor_btns, shortcuts="vscode", options={"wrap": False, "showLineNumbers": True})

    if result.get("type") == "submit":
        selected = result.get("selected", "")
        matched = False
        for key in tooltips.keys():
            if key in selected:
                matched = True
                break

        @st.dialog(f"{key}:".capitalize())
        def show_tooltip(text):
            st.info(text)

        if matched:
            show_tooltip(tooltips[key])
        else:
            show_tooltip("No tooltip available for the selected code.")

code = """
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

print(add(2, 3))
"""

tooltips = {
    "add": "Adds two numbers.",
    "multiply": "Multiplies two numbers.",
    "print": "Outputs data to the console."
}

interactive_code_with_tooltips(code, tooltips)