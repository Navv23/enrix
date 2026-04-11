import re

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_REGEX = re.compile(r"\+[1-9]\d{1,14}")
LINKEDIN_REGEX = re.compile(r"(https?:\/\/)?(www\.)?linkedin\.com\/[^\s]+")
INSTAGRAM_REGEX = re.compile(r"(https?:\/\/)?(www\.)?instagram\.com\/[^\s]+")
WHATSAPP_REGEX = re.compile(r"(https?:\/\/)?(wa\.me|whatsapp\.com)\/[^\s]+")