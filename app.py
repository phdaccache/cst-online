import streamlit as st

st.set_page_config(
    page_title='CST Online',
    initial_sidebar_state="expanded",
    page_icon=":material/robot:",
    layout="wide"
)

home = st.Page("Menu/Home.py", title="Home", icon=":material/home:", default=True)

# Sandbox
editor = st.Page("Sandbox/Editor.py", title="Editor", icon=":material/code_blocks:", default=False)

# Tutorials
reinforcement_learning = st.Page("Tutorials/Reinforcement Learning Trail.py", title="Reinforcement Learning Trail", icon=":material/developer_guide:", default=False)
attention_model = st.Page("Tutorials/The Attention Model Trail.py", title="The Attention Model Trail", icon=":material/developer_guide:", default=False)
behavior_network_model = st.Page("Tutorials/The Behavior Network Model Trail.py", title="The Behavior Network Model Trail", icon=":material/developer_guide:", default=False)
core_model = st.Page("Tutorials/The Core Model Trail.py", title="The Core Model Trail", icon=":material/developer_guide:", default=False)

pg = st.navigation(
    {
        "Menu": [home],
        "Sandbox": [editor],
        "Tutorials": [reinforcement_learning, attention_model, behavior_network_model, core_model],
    }
)

pg.run()