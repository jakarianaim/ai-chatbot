\# AI Chatbot



A simple, web-based AI chatbot built with Python, Flask, Google's Gemini API, and OpenAI API. This project serves as a personalized general AI assistant with a custom web UI and a strictly defined system persona.



\## Features

\* \*\*Multi-Model AI Integration:\*\* Uses both Google GenAI SDK (`gemini-3.8-flash`) and OpenAI API for versatile, intelligent responses.

\* \*\*Custom Web Interface:\*\* Clean, responsive chat UI built with HTML, CSS, and Vanilla JavaScript.

\* \*\*Custom Persona Injection:\*\* Configured with specific `system\_instruction` settings to maintain a unique identity (developed by Md. Jakaria Naim).

\* \*\*Error Handling:\*\* Built-in error catching and terminal logging for easy debugging.



\## Tech Stack

\* \*\*Backend:\*\* Python, Flask

\* \*\*Frontend:\*\* HTML, CSS, JavaScript

\* \*\*AI Models:\*\* Google Gemini \& OpenAI



\## Installation \& Setup



1\. \*\*Clone the repository:\*\*

&#x20;  ```bash

&#x20;  git clone \[https://github.com/jakarianaim/ai-chatbot.git](https://github.com/jakarianaim/ai-chatbot.git)

&#x20;  cd ai-chatbot

&#x20;  ```



2\. \*\*Install dependencies:\*\*

&#x20;  Make sure you have Python installed. Then, install the required packages using the terminal:

&#x20;  ```bash

&#x20;  pip install flask google-genai openai python-dotenv

&#x20;  ```



3\. \*\*Environment Setup:\*\*

&#x20;  Create a `.env` file in the root directory and add your API keys. Ensure `.env` is added to your `.gitignore` file.

&#x20;  ```env

&#x20;  GEMINI\_API\_KEY=your\_gemini\_api\_key\_here

&#x20;  OPENAI\_API\_KEY=your\_openai\_api\_key\_here

&#x20;  ```



4\. \*\*Run the application:\*\*

&#x20;  ```bash

&#x20;  python main.py

&#x20;  ```

&#x20;  Open your web browser and navigate to `http://127.0.0.1:5000` to interact with the chatbot.



\## Author

\*\*Md. Jakaria Naim\*\*

