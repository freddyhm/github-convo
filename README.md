# GitHub Conversation Starter

A web app that generates personalized conversation starters based on GitHub profiles. It analyzes a user's programming languages, contributions, and interests to create meaningful conversation topics.

# Project Goals

- Use GitHub's API to fetch user information and repositories
- Use Windsurf IDE to build project
- Use Langchain's Large Language Models to analyze the user's information and generate conversation topics

## Features

- Generate conversation starters based on most-used programming languages
- Analyze contribution patterns and project interests
- Find common repositories and topics
- Display GitHub avatar and profile information
- Modern, responsive UI built with Tailwind CSS

## Setup

1. Clone the repository
2. Create a `.env` file based on `.env.example` and add your:
   - GitHub Personal Access Token
   - OpenAI API Key

3. Install dependencies:
```bash
pipenv install
```

4. Run the application:
```bash
pipenv run python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter a GitHub username in the input field
2. Click "Analyze Profile"
3. View the generated conversation starters based on:
   - Programming languages
   - Project topics
   - General GitHub activity

## Requirements

- Python 3.13+
- GitHub Personal Access Token
- OpenAI API Key (for enhanced conversation generation)

## Dependencies

- Flask
- PyGithub
- python-dotenv
- langchain
- requests

## Architecture
- [Mermaid Architecture Diagram](architecture_mermaid.md)
- [ASCII Architecture Diagram](architecture_ascii.md)

![Draw.io Architecture Diagram](architecture.drawio.svg)

