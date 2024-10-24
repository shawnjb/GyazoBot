# Gyazo Bot (Unofficial)

The Gyazo Bot lets you connect your Gyazo account to Discord, making it easy to fetch and share images directly in your Discord chats. You can get your recent images or a random one from your Gyazo gallery.

## Features

- Connect the bot to your Gyazo account securely with your access token.
- Retrieve recent or random images from your Gyazo gallery.
- Send images as file attachments in Discord chats.

> [!IMPORTANT]
> ⚠️ The bot stores a file with user tokens in the project folder. Make sure to keep this file safe because it contains sensitive data.

## Commands

- `/authorize <token>`: Use this command to connect the bot to your Gyazo account using your access token.
- `/deauthorize`: Remove your Gyazo token and disconnect the bot from your account.
- `/lastimages <count>`: Get your most recent images (up to 10) from your Gyazo gallery.
- `/randomimage`: Get a random image from your Gyazo gallery.
- `/uploadimage [image_url] [image_file]`: Upload an image to Gyazo. You can either provide a URL or upload an image file as an attachment.

### Getting Started

1. Use `/authorize <token>` to connect the bot to your Gyazo account. If you don’t know how to get your token, leave the command blank, and the bot will give you instructions.
2. Use `/lastimages <count>` to get recent images or `/randomimage` for a random one.
3. Upload images with `/uploadimage` by either providing a URL or attaching a file.
