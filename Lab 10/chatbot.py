
HOTEL_NAME     = "Grand Élara Hotel"
HOTEL_LOCATION = "15 Rue de la Lumière, Paris, France"
HOTEL_PHONE    = "+33 1 4200 9999"
HOTEL_EMAIL    = "reservations@grandelara.com"
HOTEL_WEBSITE  = "www.grandelara.com"
CHECK_IN_TIME  = "3:00 PM"
CHECK_OUT_TIME = "12:00 PM"


def detect_intent(message):
    msg = message.lower()   

    if any(word in msg for word in ["hello", "hi", "hey", "good morning", "good evening"]):
        return "greeting"

    if any(word in msg for word in ["bye", "goodbye", "thank you", "thanks"]):
        return "farewell"

    if any(word in msg for word in ["room", "suite", "accommodation", "bed", "stay"]):
        return "rooms"

    if any(word in msg for word in ["price", "cost", "rate", "how much", "fee", "charge"]):
        return "price"

    if any(word in msg for word in ["book", "reserve", "reservation", "available"]):
        return "booking"

    if any(word in msg for word in ["check-in", "check in", "check-out", "check out", "checkin", "checkout"]):
        return "checkin"

    if any(word in msg for word in ["pool", "spa", "gym", "wifi", "wi-fi", "parking", "amenity", "amenities", "facilities"]):
        return "amenities"

    if any(word in msg for word in ["food", "eat", "restaurant", "dining", "breakfast", "lunch", "dinner", "bar", "menu"]):
        return "dining"

    if any(word in msg for word in ["location", "address", "where", "direction", "map"]):
        return "location"

    if any(word in msg for word in ["cancel", "policy", "pet", "child", "smoking", "refund"]):
        return "policy"

    if any(word in msg for word in ["contact", "phone", "email", "call", "reach"]):
        return "contact"

    return "unknown"



def get_bot_response(message):
    intent = detect_intent(message)

    if intent == "greeting":
        return (f"Welcome to {HOTEL_NAME}! \n"
                "I'm your virtual concierge. Ask me about rooms, prices, amenities, dining, or bookings!")

    if intent == "farewell":
        return f"Thank you for contacting {HOTEL_NAME}. We hope to welcome you soon! Au revoir!"

    if intent == "rooms":
        return ("We offer 5 room types:\n\n"
                " Deluxe Room       — €320/night  (Queen bed, City view, 35m²)\n"
                " Superior Room     — €420/night  (King bed, Eiffel view, 45m²)\n"
                " Junior Suite      — €620/night  (King bed, Eiffel view, 65m²)\n"
                " Grand Suite       — €950/night  (2 bedrooms, Terrace, 120m²)\n"
                " Presidential      — €2400/night (3 bedrooms, Butler, 200m²)\n\n"
                "Would you like more details about any specific room?")

    if intent == "price":
        return ("Our room rates per night:\n\n"
                "• Deluxe Room       → €320\n"
                "• Superior Room     → €420\n"
                "• Junior Suite      → €620\n"
                "• Grand Suite       → €950\n"
                "• Presidential Suite → €2,400\n\n"
                "All rates include free Wi-Fi and fitness center access.")

    if intent == "booking":
        return (f"To book a room at {HOTEL_NAME}:\n\n"
                f" Website : {HOTEL_WEBSITE}\n"
                f" Phone   : {HOTEL_PHONE}\n"
                f" Email   : {HOTEL_EMAIL}\n\n"
                "Free cancellation is available up to 48 hours before arrival.")

    if intent == "checkin":
        return (f"Our timings are:\n\n"
                f"Check-in  : {CHECK_IN_TIME}\n"
                f" Check-out : {CHECK_OUT_TIME}\n\n"
                "Early check-in (€60) and late check-out (€80) are available on request.")

    if intent == "amenities":
        return ("Our amenities include:\n\n"
                "✦ Rooftop infinity pool (7am – 10pm)\n"
                "✦ Le Ciel Spa & Wellness (9am – 9pm)\n"
                "✦ 24/7 Fitness center\n"
                "✦ Free high-speed Wi-Fi\n"
                "✦ Valet parking (€45/night)\n"
                "✦ Airport limousine (€180)\n"
                "✦ Business center & meeting rooms\n"
                "✦ Pet-friendly rooms available")

    if intent == "dining":
        return ("Our dining options:\n\n"
                "  L'Élara Restaurant  — Fine French cuisine (7am–11pm)\n"
                "  Le Bar Doré         — Cocktails & live jazz (5pm–1am)\n"
                "  Room Service        — Available 24/7\n"
                "  Breakfast Buffet    — €38 per person\n\n"
                "Reservations recommended for the restaurant.")

    if intent == "location":
        return (f" We are located at:\n{HOTEL_LOCATION}\n\n"
                "5-minute walk from Champs-Élysées\n"
                "10 minutes from the Eiffel Tower\n\n"
                f"Airport transfer available for €180. Call {HOTEL_PHONE} to arrange pickup.")

    if intent == "policy":
        return ("Our key policies:\n\n"
                " Cancellation : Free up to 48 hours before arrival\n"
                " Children     : Under 12 stay free\n"
                " Pets         : Welcome (€30/night supplement)\n"
                " Smoking      : Non-smoking property\n"
                " Minimum age  : 18 years to book")

    if intent == "contact":
        return (f" Phone   : {HOTEL_PHONE}\n"
                f" Email   : {HOTEL_EMAIL}\n"
                f" Website : {HOTEL_WEBSITE}\n\n"
                "Our front desk is available 24/7.")

    return ("I'm sorry, I didn't understand that. \n\n"
            "I can help you with:\n"
            " Room types & pricing\n"
            " Bookings & reservations\n"
            " Check-in / Check-out times\n"
            " Amenities & facilities\n"
            " Dining options\n"
            " Location & directions\n"
            " Hotel policies & contact")