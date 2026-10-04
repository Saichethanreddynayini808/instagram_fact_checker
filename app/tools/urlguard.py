"""
STEP 6. Safety: refuse URLs the server must never fetch.

Only http/https. No localhost, private or link-local IPs (checked after DNS
resolution), no redirects into those ranges.
"""
