"""
- same request -> same key; changed prompt file or model -> different key
- record then replay returns the saved value
- replay miss raises (never silently calls the API)
"""
