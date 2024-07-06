responses = {
    "operating_hours": "Our operating hours are from 9 AM to 5 PM, Monday to Friday.",
    "reset_password": "You can reset your password by clicking on the 'Forgot Password' link on the login page.",
    "pricing": "Our pricing varies depending on the service. Please visit our pricing page for more details.",
    "contact_info": "You can contact us at support@example.com or call us at 123-456-7890.",
    "office_location": "Our office is located at 123 Main Street, Hometown, USA.",
    "support_offering": "We offer 24/7 customer support through chat and email."
}

def generate_response(intent):
    return responses.get(intent, "I'm not sure how to help with that.")