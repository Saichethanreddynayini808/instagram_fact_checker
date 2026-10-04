"""
- tavily times out -> retried -> serper answers
- 401 from tavily: not retried, goes straight to serper
- both fail -> SearchFailed with a reason, no exception escapes
"""
