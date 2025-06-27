from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


# Маршрут для отправки сообщений в Telegram
@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    fullname = data.get('fullname')
    email = data.get('email')
    message = data.get('message')

    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    text = f"New Contact Form Submission:\n\nName: {fullname}\nEmail: {email}\nMessage: {message}"

    try:
        response = requests.post(
            f'https://api.telegram.org/bot{bot_token}/sendMessage',
            json={'chat_id': chat_id, 'text': text}
        )
        if response.status_code == 200:
            return jsonify({'message': 'Message sent successfully!'}), 200
        else:
            return jsonify({'error': 'Failed to send message.'}), 500
    except Exception as e:
        print(e)
        return jsonify({'error': 'An error occurred.'}), 500

# Запуск сервера
if __name__ == "__main__":
    app.run(debug=True)
