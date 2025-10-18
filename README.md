 [AI Interviewer Thumbnail](AI Interviewer_RejaRony.png)
 # AI Interviewer

👉 **LIVE DEMO:** [Try the Interviewer Here!](https://ai-interviewer-rejarony.onrender.com) 👈

This project implements an AI interviewer that can conduct mock interviews and provide instant, semantic feedback on candidate answers 
using advanced Natural Language Processing (NLP) techniques.. It utilizes Python and the Flask framework to create a web application for a seamless user experience.

## Key Features

* **Semantic Scoring:** Utilizes NLP (Cosine Similarity) for advanced answer evaluation.
* **Full-Stack Implementation:** Built with Python (Flask) backend and a responsive front-end (HTML/CSS/JS).
* **Session Management:** Tracks user progress and calculates a final score.
* **Modular Code:** Easy to extend and integrate with LLMs (e.g., Gemini API) in the future.

## Technologies Used

* Python (Backend Logic)

* Flask (Micro Web Framework)

* NLTK, Scikit-learn (Advanced NLP for Semantic Similarity Scoring)

* HTML/CSS/JavaScript (Responsive Chat Interface)

## Setup Instructions

Follow these steps to set up the project:

1.  **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    ```

2.  **Activate the virtual environment:**

    *   **On macOS and Linux:**

        ```bash
        source venv/bin/activate
        ```

    *   **On Windows:**

        ```bash
        .\venv\Scripts\activate
        ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

Once the dependencies are installed, you can run the application using Flask:

flask run

This will start the development server.  You can then access the application in your web browser, usually at `http://127.0.0.1:5000`.

## Contributing

We welcome contributions to this project!  If you'd like to contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with descriptive commit messages.
4.  Test your changes thoroughly.
5.  Submit a pull request to the main branch.

Please ensure your code adheres to the project's coding style and includes appropriate tests.

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute this code. - see the [LICENSE](LICENSE) file for details.
