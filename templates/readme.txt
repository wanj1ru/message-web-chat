# Messaging Web App

This is a simple messaging web application built using Flask, a micro web framework for Python. The application allows users to send and receive messages, search for messages, and interact with messages through a web interface or API.

## Features

- **User Authentication**: Users can register, login, and logout to access the messaging functionality.
- **Sending Messages**: Users can send messages through a web form interface.
- **Receiving Messages**: Users can receive messages and view them through a web form interface.
- **API Integration**: Messages can be sent and received via API endpoints.
- **Database Integration**: Messages are stored in an SQLite database.
- **Search Messages**: Users can search for messages containing specific keywords.
- **Agent Portal**: An agent portal allows authorized users to view all messages in the system and respond to them.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your_username/messaging-web-app.git
    ```

2. Navigate to the project directory:

    ```bash
    cd messaging-web-app
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:

    ```bash
    python app.py
    ```

5. Access the application in your web browser at `http://localhost:5000`.

## Usage

- **Register/Login**: Create an account or log in to access the messaging functionality.
- **Send Message**: Navigate to the "Send Message" page to compose and send a message.
- **Receive Message**: Navigate to the "Receive Message" page to view messages received.
- **API Integration**: Utilize the API endpoints `/api/message` and `/api/send_message` to send and receive messages programmatically.
- **Search Messages**: Use the search functionality to find messages containing specific keywords.
- **Agent Portal**: Authorized users can access the agent portal to view and respond to all messages in the system.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to customize and extend this messaging web application according to your requirements! If you encounter any issues or have suggestions for improvement, please [open an issue](https://github.com/your_username/messaging-web-app/issues).