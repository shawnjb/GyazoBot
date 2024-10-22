# Gyazo Bot (Unofficial)

Gyazo Bot allows you to authorize and fetch images from your Gyazo account, including random and recent images, directly within Discord. Please refrain from using this bot or the images it retrieves for AI training data or any machine learning purposes.

## Features

- Securely authorize the bot with your Gyazo access token.
- Retrieve the most recent or a random image from your Gyazo gallery.
- Receive images as file attachments in Discord.

> [!CAUTION]
> This bot stores a database file in the project directory, which is generally excluded from version control using `.gitignore`. Make sure that this file is kept secure, as it contains sensitive data that could provide access to Gyazo accounts.

## Getting Started

1. Use the `/authorize <token>` command to grant access to the bot. If you need help, do not provide a token and it will show instructions.
2. Use `/lastimages <count>` to retrieve recent images or `/randomimage` for a random image.
