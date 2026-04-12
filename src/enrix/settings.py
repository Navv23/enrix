import re

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_REGEX = re.compile(r"(?<!\w)\+(?:[1-9]\d{0,2})[\s\-\.]?(?:\(?\d{1,4}\)?[\s\-\.]?){1,3}\d{3,4}(?!\w)")
LINKEDIN_REGEX = re.compile(r"(https?:\/\/)?(www\.)?linkedin\.com\/[^\s]+")
INSTAGRAM_REGEX = re.compile(r"(https?:\/\/)?(www\.)?instagram\.com\/[^\s]+")
WHATSAPP_REGEX = re.compile(r"(https?:\/\/)?(wa\.me|whatsapp\.com)\/[^\s]+")