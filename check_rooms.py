import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

URL = "https://online.maavaishnodevi.org/api/v1/eAccommodation/accomAvailability"

PAYLOAD = {
    "locationId": "3",
    "accomTypeId": "1",
    "accomDate": "2026-11-09",
    "noOfDays": "1",
}

SMTP_HOST = os.environ["SMTP_HOST"]
SMTP_PORT = int(os.environ["SMTP_PORT"])
EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
EMAIL_TO = os.environ["EMAIL_TO"]
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def check_rooms():
    response = requests.post(
        URL,
        json=PAYLOAD,
        timeout=30,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
        },
    )
    response.raise_for_status()
    data = response.json()

    rooms = data.get("accomAvailOp")
    available_rooms = []

    if data.get("flag") == "N" and rooms:
        for room in rooms:
            if room.get("noOfAvailable", 0) > 0:
                available_rooms.append(room)

    return data, available_rooms


def send_email(rooms):
    subject = "🚨 Vaishno Devi Room Available!"

    body = "Rooms are available for 9 November 2026:\n\n"

    for room in rooms:
        body += (
            f"Guest House: {room.get('guestHouseName')}\n"
            f"Room: {room.get('accomName')}\n"
            f"Available: {room.get('noOfAvailable')}\n"
            f"Price: ₹{room.get('rentalAmount')}\n"
            f"Quota ID: {room.get('quotaId')}\n"
            f"Accom ID: {room.get('accomId')}\n\n"
        )

    body += "Check the official Vaishno Devi accommodation portal."

    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

def send_telegram(rooms):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    message = "🚨 *VAISHNO DEVI ROOM AVAILABLE!*\n\n"

    for room in rooms:
        message += (
            f"🏠 *{room.get('guestHouseName')}*\n"
            f"🛏️ {room.get('accomName')}\n"
            f"🟢 Available: {room.get('noOfAvailable')}\n"
            f"💰 ₹{room.get('rentalAmount')}\n"
            f"📅 {room.get('accomDate')}\n\n"
        )

    message += "⚡ Book it quickly!"

    response = requests.post(
        url,
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown",
        },
        timeout=30,
    )

    response.raise_for_status()
if __name__ == "__main__":
    data, rooms = check_rooms()

    print("API response:")
    print(data)

    if rooms:
        print("\n🚨 ROOMS AVAILABLE!")
        for room in rooms:
            print(
                room.get("guestHouseName"),
                "|",
                room.get("accomName"),
                "| Available:",
                room.get("noOfAvailable"),
            )

        send_email(rooms)
        print("Email sent.")
        
        send_telegram(rooms)
        print("Telegram message sent.")
    else:
        print("\n❌ No rooms available.")
