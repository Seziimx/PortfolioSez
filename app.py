from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import requests

app = Flask(__name__, static_folder='.', static_url_path='')

# Маршрут для главной страницы
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

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
if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
