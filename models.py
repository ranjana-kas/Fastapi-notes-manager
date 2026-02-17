from typing import TypedDict
from datetime import datetime

# This defines the "Shape" of our internal data.
# It enforces that every note in our storage list must look exactly like this.
class Note(TypedDict):
    id: int
    title: str
    content: str
    created_at: datetime  # <--- New
    updated_at: datetime  # <--- New