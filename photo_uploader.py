import streamlit as st
import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Replace with your bot's token and chat ID
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = '723824465'


def send_photo_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    # Prepare the file
    files = {'photo': open(file_path, 'rb')}

    # Prepare the payload with the inline keyboard
    payload = {
        'chat_id': CHAT_ID,
        'caption': '',
        'reply_markup': json.dumps({
            'inline_keyboard': [
                [{'text': 'Positive', 'callback_data': 'positive'},
                 {'text': 'Negative', 'callback_data': 'negative'},
                 {'text': 'Error', 'callback_data': 'error'}]
            ]
        })
    }

    # Send the request to Telegram
    response = requests.post(url, files=files, data=payload)

    # Close the file after sending
    files['photo'].close()

    return response


def main():
    st.title("Photo Uploader for Telegram")

    uploaded_file = st.file_uploader("Choose a photo...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        file_path = os.path.join("temp", uploaded_file.name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.image(file_path, caption='Uploaded Photo', use_column_width=True)
        st.write("")

        if st.button("Send to Telegram"):
            response = send_photo_to_telegram(file_path)
            if response.status_code == 200:
                st.success("Photo sent to Telegram!")
            else:
                st.error("Failed to send photo to Telegram.")


if __name__ == "__main__":
    main()
