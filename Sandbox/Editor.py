import streamlit as st
import os
import tempfile
import shutil
from code_editor import code_editor
import json

JAVA11 = "/usr/lib/jvm/java-11-openjdk-amd64"
JAVA17 = "/usr/lib/jvm/java-17-openjdk-amd64"

# function that creates temp dir and copies the project
def create_temp_dir(project_name):
    temp_dir = tempfile.mkdtemp()
    # Copy the project into the temp directory
    src_path = os.path.abspath(project_name)
    dst_path = os.path.join(temp_dir, project_name)
    shutil.copytree(src_path, dst_path, dirs_exist_ok=True, ignore=shutil.ignore_patterns('*.iml', '*.log', '*.class'))
    return dst_path

def prepare_and_build_project(path, java_version):
    # Fix script permissions and line endings
    gradlew_path = os.path.join(path, "gradlew")
    os.system(f"chmod +x {gradlew_path}")
    os.system(f"sed -i 's/\\r$//' {gradlew_path}")

    # Build the JAR
    os.environ["JAVA_HOME"] = java_version
    build_cmd = f"cd {path} && ./gradlew build"
    build_result = os.system(build_cmd)

    # Return path to built JAR if successful
    if build_result == 0:
        jar_path = os.path.join(path, "build", "libs")
        for file in os.listdir(jar_path):
            if file.endswith("-full.jar"):
                return os.path.join(jar_path, file)
    return None

def build_ws3d(temp_dir):
    if st.button("Build ws3d JAR"):
        with st.spinner("Building..."):
            try:
                jar_file_path = prepare_and_build_project(temp_dir, JAVA11)
            except Exception as e:
                st.error(f"Build failed: {e}")
                return None

        return jar_file_path

def download_ws3d(jar_file_path):
    if jar_file_path:
        with open(jar_file_path, "rb") as fp:
            st.download_button(
                label="Download ws3d JAR",
                data=fp,
                file_name="ws3d.jar",
            )

def build_democst(temp_dir):
    if st.button("Build DemoCST JAR"):
        with st.spinner("Building..."):
            try:
                jar_file_path = prepare_and_build_project(temp_dir, JAVA17)
            except Exception as e:
                st.error(f"Build failed: {e}")
                return None

        return jar_file_path
    
def download_democst(jar_file_path):
    if jar_file_path:
        with open(jar_file_path, "rb") as fp:
            st.download_button(
                label="Download DemoCST JAR",
                data=fp,
                file_name="democst.jar",
            )

# Step 1: File Browser
def get_all_files_and_dirs(base_path):
    items = []
    for root, dirs, files in os.walk(base_path):
        for f in files:
            rel_path = os.path.relpath(os.path.join(root, f), base_path)
            items.append(rel_path)
    return sorted(items)

def file_tree(base_path, rel_path="", level=0, key=""):
    current_path = os.path.join(base_path, rel_path)
    entries = sorted(os.listdir(current_path))

    # Separate folders and files
    folders = [e for e in entries if os.path.isdir(os.path.join(current_path, e))]
    files = [e for e in entries if not os.path.isdir(os.path.join(current_path, e))]

    # Render folders first
    for entry in folders:
        full_path = os.path.join(current_path, entry)
        rel_entry_path = os.path.join(rel_path, entry)
        indent = " " * level  # em-space

        key = f"toggle_{rel_entry_path}" + key
        is_open = st.session_state.get(key, False)
        if st.button(f"{indent}📁 {entry}", key=key + "_btn"):
            st.session_state[key] = not is_open
        if st.session_state.get(key, False):
            file_tree(base_path, rel_entry_path, level + 1)

    # Then render files
    for entry in files:
        rel_entry_path = os.path.join(rel_path, entry)
        indent = " " * level
        if st.button(f"{indent}📄 {entry}", key=f"file_{rel_entry_path}" + key):
            st.session_state["selected_file"] = os.path.join(base_path, rel_entry_path)

def find_first_file(base_path):
    for root, dirs, files in os.walk(base_path):
        if files:
            return os.path.join(root, files[0])
    return None

def display_code_editor(code, file_name, button, command, button_message, ace_props=None):
    # --- Editor Config ---
    editor_btns = [{
        "name": f"{button}",
        "feather": f"{button}",
        "primary": True,
        "hasText": True,
        "showWithIcon": True,
        "alwaysOn": True,
        "commands": [f"{command}", 
                 ["infoMessage", 
                  {
                   "text":f"{button_message}",
                   "timeout": 2500, 
                   "classToggle": "show",
                  }
                 ]
                ],
        "style": {"top": "-0.25rem", "right": "0.4rem"}
    }]

    # response_dict = code_editor(
    #     code,
    #     height=[10, 17],
    #     lang="java",
    #     theme="default",
    #     shortcuts="vscode",
    #     focus=False,
    #     buttons=editor_btns,
    #     options={"wrap": True, "showLineNumbers": True}
    # )

    info_bar = {
        "name": "file info",
        "css": "\nbackground-color: #bee1e5;\n\nbody > #root .ace-streamlit-dark~& {\n   background-color: #262830;\n}\n\n.ace-streamlit-dark~& span {\n   color: #fff;\n    opacity: 0.6;\n}\n\nspan {\n   color: #000;\n    opacity: 0.5;\n}\n\n.code_editor-info.message {\n    width: inherit;\n    margin-right: 75px;\n    order: 2;\n    text-align: center;\n    opacity: 0;\n    transition: opacity 0.7s ease-out;\n}\n\n.code_editor-info.message.show {\n    opacity: 0.6;\n}\n\n.ace-streamlit-dark~& .code_editor-info.message.show {\n    opacity: 0.5;\n}\n",
        "style": {
            "order": "1",
            "display": "flex",
            "flexDirection": "row",
            "alignItems": "center",
            "width": "100%",
            "height": "2.5rem",
            "padding": "0rem 0.6rem",
            "padding-bottom": "0.2rem",
            "margin-bottom": "-1px",
            "borderRadius": "8px 8px 0px 0px",
            "zIndex": "9993"
        },
        "info": [{
            "name": f"{file_name}",
            "style": {"width": "100px"}
        }]
    }
    info_bar["style"] = {**info_bar["style"], "order": "1", "height": "2.0rem", "padding": "0rem 0.6rem", "padding-bottom": "0.2rem"}
    response_dict = code_editor(code,  height = [15, 17], theme="default", lang="java", shortcuts="vscode", buttons=editor_btns, info=info_bar, options={"wrap": False, "showLineNumbers": True}, props=ace_props)

    # --- Handle Save ---
    if response_dict.get("type") == "submit":
        updated_code = response_dict.get("text", "")
        
        # Update session state and save to file
        st.session_state.file_code[selected_file] = updated_code
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_code)

if "democst_dir" not in st.session_state:
    st.session_state.democst_dir = create_temp_dir("DemoCST")
if "ws3d_dir" not in st.session_state:
    st.session_state.ws3d_dir = create_temp_dir("ws3d")

SRC_DIR = os.path.join(st.session_state.democst_dir, "src/main/java")

if "selected_file" not in st.session_state:
    first_file = find_first_file(SRC_DIR)
    st.session_state["selected_file"] = first_file


with st.expander("File Browser", expanded=False, icon="📂"):
    file_tree(SRC_DIR)
    selected_file = st.session_state["selected_file"]


tab1, tab2, tab3 = st.tabs(["📝 Edit Files", "🔄 Change Files", "🛠️ Build & Download"])

with tab1:
    # Step 2: Edit File
    # st.subheader(f"📝 File: `{os.path.basename(selected_file)}`")

    file_path = os.path.join(SRC_DIR, selected_file)
    if os.path.isfile(file_path):
        # --- Session key for content ---
        if "file_code" not in st.session_state:
            st.session_state.file_code = {}

        # Load file content if not already loaded or if user changed file
        if selected_file not in st.session_state.file_code:
            with open(file_path, "r", encoding="utf-8") as f:
                st.session_state.file_code[selected_file] = f.read()

        code = st.session_state.file_code[selected_file]

        ace_props = {"style": {"borderRadius": "0px 0px 8px 8px"}}
        display_code_editor(code, os.path.basename(selected_file), "Save", "submit", "Saved!", ace_props)

with tab2:
    # Step 3: Add New File
    st.subheader("📄 Create New File")
    new_file_path = st.text_input("Relative to `DemoCST/src/main/java`", help="Example: `codelets/behaviors/MyNewBehavior.java`)")

    if st.button("➕ Create File"):
        full_path = os.path.join(SRC_DIR, new_file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        @st.dialog("Status:")
        def status1(path):
            if path != None:
                st.success(f"File Created: {path}")
            else:
                st.warning("File already exists.")
            if st.button("Ok"):
                st.rerun()

        if not os.path.exists(full_path):
            with open(full_path, "w", encoding="utf-8") as f:
                f.write("// New Java file\n")
            status1(new_file_path)
        else:
            status1(None)

    st.divider()

    # Step 4: Delete File/Folder
    file_list = get_all_files_and_dirs(SRC_DIR)

    st.subheader("🗑️ Delete File or Folder")

    st.write(f"Delete `{os.path.basename(selected_file)}`?")

    @st.dialog("Status:")
    def status2(path):
        if path != None:
            st.success(f"Deleted: {path}")
        else:
            st.warning("Invalid selection.")
        if st.button("Ok"):
            st.rerun()

    if st.button("❌ Delete"):
        if os.path.isfile(selected_file):
            os.remove(selected_file)
            status2(os.path.basename(selected_file))
        elif os.path.isdir(selected_file):
            import shutil
            shutil.rmtree(selected_file)
            status2(os.path.basename(selected_file))
        else:
            status2(None)

with tab3:
    with st.expander(f"Preview"):
        file_path = os.path.join(SRC_DIR, selected_file)
        if os.path.isfile(file_path):
            # --- Session key for content ---
            if "file_code" not in st.session_state:
                st.session_state.file_code = {}

            # Load file content if not already loaded or if user changed file
            if selected_file not in st.session_state.file_code:
                with open(file_path, "r", encoding="utf-8") as f2:
                    st.session_state.file_code[selected_file] = f2.read()

            code2 = st.session_state.file_code[selected_file]

            ace_props = {"style": {"borderRadius": "0px 0px 8px 8px"}}
            display_code_editor(code2, os.path.basename(selected_file), "Copy", "copyAll", "Copied to clipboard!", ace_props)

    jar_file_path_ws3d = build_ws3d(st.session_state.ws3d_dir)
    download_ws3d(jar_file_path_ws3d)
    jar_file_path_democst = build_democst(st.session_state.democst_dir)
    download_democst(jar_file_path_democst)