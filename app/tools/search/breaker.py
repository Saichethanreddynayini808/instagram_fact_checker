"""
STEP 5. Circuit breaker. Opens after 3 failures, 60 s cooldown, then one
trial call. Takes a clock function so tests do not need to sleep.
"""
