const express = require('express');
const fetch = require('node-fetch');
require('dotenv').config();

const app = express();
app.use(express.json()); // Для обработки JSON-запросов

// Обработчик POST-запроса для отправки сообщения в Telegram
app.post('/send-message', async (req, res) => {
    const { fullname, email, message } = req.body;
    const botToken = process.env.TELEGRAM_BOT_TOKEN; // Токен бота из переменных окружения
    const chatId = process.env.TELEGRAM_CHAT_ID; // Chat ID из переменных окружения

    const text = `New Contact Form Submission:\n\nName: ${fullname}\nEmail: ${email}\nMessage: ${message}`;

    try {
        const response = await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: chatId, text: text }),
        });

        if (response.ok) {
            res.status(200).send('Message sent successfully!');
        } else {
            res.status(500).send('Failed to send message.');
        }
    } catch (error) {
        console.error(error);
        res.status(500).send('An error occurred.');
    }
});

// Запуск сервера
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));