# Economics Practice Platform

A comprehensive online platform for economics students to practice with official past papers from major exams. The platform supports AP Economics, IGCSE Cambridge Economics, A-level Economics, and DSE Economics.

## Features

- **Official Past Papers**: Practice with authentic exam questions
- **Instant Feedback**: Get immediate and accurate feedback on your answers
- **Wrong Question Analysis**: Receive targeted similar questions to strengthen weak areas
- **Bilingual Support**: Available in both English and Chinese
- **Responsive Design**: Optimized for desktop and tablet use
- **Clean Interface**: Simple and intuitive operation with no redundant features

## Supported Exams

- AP Economics (Micro + Macro)
- IGCSE Cambridge Economics
- A-level Economics (AS + A2)
- DSE Economics

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, Jinja2 templates
- **Internationalization**: Flask-Babel

## Project Structure

```
Economics Practice Platform/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── templates/          # HTML templates
    ├── base.html       # Base template with common structure
    ├── index.html      # Home page
    ├── select_exam.html # Exam type selection page
    ├── practice.html   # Practice page with questions
    ├── practice_result.html # Practice results page
    ├── wrong_questions.html # Wrong questions collection
    └── similar_questions.html # Similar questions page
```

## Getting Started

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Installation

1. Clone the repository or download the project files

2. Navigate to the project directory:
   ```bash
   cd Economics Practice Platform
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the Flask development server:
   ```bash
   python app.py
   ```

2. Open your web browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

## Usage

1. **Select Language**: Choose between English and Chinese using the language selector in the header

2. **Choose Exam Type**: Select the exam you want to practice from the available options

3. **Practice Questions**: Answer the questions presented on the practice page

4. **Submit Answers**: Click the "Submit Answers" button to get feedback

5. **Review Results**: Check your score and detailed explanations for each question

6. **Practice Similar Questions**: For incorrect answers, practice similar questions to improve

7. **View Wrong Questions**: Access your collection of wrong questions from the navigation

## Customization

### Adding More Questions

To add more questions to the platform, edit the `QUESTION_BANK` dictionary in `app.py`. Each question should follow this structure:

```python
{
    'id': 1,              # Unique question ID
    'question': '...',    # Question text
    'options': ['...'],   # List of answer options
    'answer': 'A',        # Correct answer
    'explanation': '...', # Detailed explanation
    'topic': '...'        # Topic for similar question matching
}
```

### Adding New Exam Types

To add support for a new exam type, add a new key to the `QUESTION_BANK` dictionary in `app.py` and update the `select_exam.html` template to include the new exam option.

## Deployment

For production deployment, it is recommended to use a WSGI server like Gunicorn and a reverse proxy like Nginx. Here's a basic deployment guide:

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Run the application with Gunicorn:
   ```bash
   gunicorn app:app --workers 4
   ```

3. Configure Nginx to act as a reverse proxy (example configuration):
   ```nginx
   server {
       listen 80;
       server_name example.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
