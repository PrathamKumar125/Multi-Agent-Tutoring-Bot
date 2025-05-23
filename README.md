# Multi-Agent Tutoring Bot

A sophisticated tutoring system built with LangChain, Ollama, and Gradio that uses specialized AI agents to help students with mathematics and physics questions.




https://github.com/user-attachments/assets/34c97ff0-d9d2-4574-ba78-093556309d49

Deployed URL: https://multi-agent-tutoring-bot-production-da1f.up.railway.app/

**⚠️ Note:** This app is hosted on a free-tier deployment environment with limited hardware resources, which may lead to slower response times. For best performance, consider running the app locally.

---
## Architecture

### Main Components

1. **Tutor Agent** - Primary orchestrator that routes queries to specialist agents
2. **Math Agent** - Specialized in mathematics with calculator tool integration
3. **Physics Agent** - Specialized in physics with constants lookup tool
4. **Tools** - Calculator and physics constants database

### Agent Communication Flow

```
User Query → Tutor Agent → Classification → Specialist Agent → Tool Usage → Response
```

## Features

- **Intelligent Query Routing**: Automatically determines whether a question is about math, physics, or general topics
- **Specialized Agents**: Dedicated agents for mathematics and physics with domain-specific knowledge
- **Tool Integration**:
  - Calculator tool for mathematical computations
  - Physics constants database for scientific calculations
- **Interactive Web Interface**: User-friendly Gradio interface with conversation history
- **Educational Focus**: Provides step-by-step explanations and learning support

## Prerequisites

1. **Option 1 (Docker)**: Docker and Docker Compose installed
2. **Option 2 (Local)**:
   - Python 3.8+
   - Ollama installed and running
   - Qwen3:0.6b model pulled in Ollama

### Install Ollama and Model (for local installation)

```bash
# Install Ollama (visit https://ollama.ai for platform-specific instructions)
# Pull the required model
ollama pull qwen3:0.6b
```

## Installation

### Option 1: Using Docker Compose (Recommended)

This method will set up both the tutoring bot and Ollama in separate containers:

1. **Clone or download the project**
2. **Run Docker Compose**:
```bash
docker-compose up
```
3. **Open your browser** to `http://localhost:7860`

### Option 2: Using Docker Compose with Local Ollama

If you already have Ollama running locally:

1. **Ensure Ollama is running with the required model**:
```bash
ollama run qwen3:0.6b
```

2. **Run the Docker container using the local Ollama compose file**:
```bash
docker-compose -f docker-compose.local-ollama.yml up
```

3. **Open your browser** to `http://localhost:7860`

### Option 3: Using Docker Directly with Local Ollama

If you prefer to use Docker commands directly:

1. **Ensure Ollama is running with the required model**:
```bash
ollama run qwen3:0.6b
```

2. **Build and run the Docker container**:
```bash
docker build -t tutoring-bot .
docker run -p 7860:7860 -e OLLAMA_BASE_URL=http://host.docker.internal:11434 --add-host=host.docker.internal:host-gateway tutoring-bot
```

3. **Open your browser** to `http://localhost:7860`

### Option 3: Local Installation

1. **Clone or download the project**
2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Ensure Ollama is running**:
```bash
ollama serve
```

## Usage

1. **Start the application** (if using local installation):
```bash
python app.py
```

2. **Open your browser** to the appropriate URL (based on installation method)

3. **Ask questions** like:
   - "Solve 2x + 5 = 11"
   - "What is Newton's second law?"
   - "Calculate 15 × 23"
   - "What is the speed of light?"

## 🔧 Configuration

Edit `config.py` to modify:
- Ollama base URL
- Model name
- Physics constants database
- Agent behavior parameters

## Project Structure

```
Multi-Agent Tutoring Bot/
├── agents/
│   ├── tutor_agent.py      # Main orchestrating agent
│   ├── math_agent.py       # Mathematics specialist
│   └── physics_agent.py    # Physics specialist
├── tools/
│   ├── calculator.py       # Calculator tool for math
│   └── physics_constants.py # Constants lookup tool
├── config.py                      # Configuration settings
├── app.py                         # Main Gradio application
├── requirements.txt               # Dependencies
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Docker Compose configuration with Ollama
├── docker-compose.local-ollama.yml # Docker Compose for local Ollama
├── setup-ollama.sh                # Script to set up Ollama (Linux/Mac)
├── setup-ollama.bat               # Script to set up Ollama (Windows)
├── .dockerignore                  # Files to exclude from Docker build
└── README.md                      # This file
```

