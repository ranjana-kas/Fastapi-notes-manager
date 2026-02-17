import streamlit as st
import os

# CONFIGURATION
# We look for the API_URL in Streamlit's secrets (Cloud)
# If not found, we default to Localhost (Local testing)
if "API_URL" in st.secrets:
    API_URL = st.secrets["API_URL"]
else:
    API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Notes Manager Pro", page_icon="📝", layout="centered")

# ------------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------------
def get_notes(search_query=None):
    """Fetch notes from the API, optionally filtering by a query."""
    try:
        if search_query:
            # Uses the new Search Endpoint
            response = requests.get(f"{API_URL}/notes/search", params={"query": search_query})
        else:
            # Uses the standard Get All Endpoint
            response = requests.get(f"{API_URL}/notes/")
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch notes.")
            return []
    except requests.exceptions.ConnectionError:
        st.error("🔌 API is offline. Make sure your FastAPI server is running!")
        return []

def create_note(title, content):
    """Send a POST request to create a new note."""
    payload = {"title": title, "content": content}
    response = requests.post(f"{API_URL}/notes/", json=payload)
    return response.status_code == 201

def update_note(note_id, title, content):
    """Send a PUT request to update an existing note."""
    payload = {"title": title, "content": content}
    response = requests.put(f"{API_URL}/notes/{note_id}", json=payload)
    return response.status_code == 200

def delete_note(note_id):
    """Send a DELETE request to remove a note."""
    response = requests.delete(f"{API_URL}/notes/{note_id}")
    return response.status_code == 200

# ------------------------------------------------------------------
# UI LAYOUT
# ------------------------------------------------------------------
st.title("📝 Notes Manager")

# --- SIDEBAR: CREATE NOTE ---
with st.sidebar:
    st.header("➕ Create New Note")
    
    # We use a form here so the page doesn't reload on every keystroke
    with st.form("create_form", clear_on_submit=True):
        new_title = st.text_input("Title")
        new_content = st.text_area("Content")
        
        # This is the specific submit button for the sidebar form
        submitted = st.form_submit_button("Add Note")
        
        if submitted:
            if new_title and new_content:
                if create_note(new_title, new_content):
                    st.success("✅ Note created!")
                    st.rerun() # Refresh to show the new note immediately
                else:
                    st.error("❌ Failed to create note.")
            else:
                st.warning("⚠️ Title and Content are required.")

# --- MAIN AREA: SEARCH ---
search_query = st.text_input("🔍 Search your notes...", placeholder="Type title or content...")

# --- FETCH DATA ---
notes = get_notes(search_query)

# --- DISPLAY RESULTS ---
st.divider()

if not notes:
    st.info("No notes found.")
else:
    # Show count
    count = len(notes)
    st.caption(f"Found {count} {'note' if count == 1 else 'notes'}")

    # Iterate through notes and display them
    for note in notes:
        # We use an Expander to hide details until clicked
        with st.expander(f"📌 {note['title']}"):
            
            # --- VIEW METADATA ---
            st.markdown(f"**ID:** `{note['id']}`")
            st.caption(f"Created: {note['created_at']}")
            
            # --- UPDATE FORM ---
            st.subheader("Edit Note")
            
            # CRITICAL: We create a unique form key for every note using its ID
            with st.form(key=f"edit_form_{note['id']}"):
                
                # Input fields pre-filled with current data
                edit_title = st.text_input("Title", value=note['title'])
                edit_content = st.text_area("Content", value=note['content'], height=150)
                
                # The Submit Button (Must be inside st.form)
                save_btn = st.form_submit_button("💾 Save Changes")
                
                if save_btn:
                    if update_note(note['id'], edit_title, edit_content):
                        st.success("✅ Updated successfully!")
                        st.rerun() # Refresh page to see changes
                    else:
                        st.error("❌ Update failed.")
            
            # --- DELETE ACTION ---
            # This is OUTSIDE the form because it's a separate destructive action
            st.write("") 
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("🗑️ Delete Note", key=f"del_{note['id']}"):
                    if delete_note(note['id']):
                        st.success("Deleted!")
                        st.rerun()