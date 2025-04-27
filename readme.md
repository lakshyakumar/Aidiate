# Aidiate: Your Lean-Stack AI Companion

Aidiate is a lightweight, AI-powered service designed to assist with idea generation, brainstorming, and managing your creative workflows. Built with FastAPI, it integrates AI capabilities and a MongoDB backend to provide a seamless experience for managing and enhancing your ideas.

## Features

- **AI-Powered Idea Generation**: Leverage AI to brainstorm and refine your ideas.
- **Idea Management**: Store, retrieve, and manage your ideas in a MongoDB database.
- **Health Check Endpoint**: Verify the service's health and availability.
- **RESTful API**: Easy-to-use endpoints for interacting with the service.
- **Extensible Graph Framework**: Build and execute workflows using a graph-based architecture.

## Project Structure

```plaintext
.
├── .env                # Environment variables
├── .gitignore          # Git ignore rules
├── .vscode/            # VS Code settings
│   └── settings.json
├── Dockerfile          # Docker configuration
├── [env.sample](http://_vscodecontentref_/#%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22d%3A%5C%5Ccode%5C%5CAI%5C%5Caideate%5C%5Cenv.sample%22%2C%22_sep%22%3A1%2C%22path%22%3A%22%2FD%3A%2Fcode%2FAI%2Faideate%2Fenv.sample%22%2C%22scheme%22%3A%22file%22%7D%7D)          # Sample environment variables
├── [main.py](http://_vscodecontentref_/#%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22d%3A%5C%5Ccode%5C%5CAI%5C%5Caideate%5C%5Cmain.py%22%2C%22_sep%22%3A1%2C%22path%22%3A%22%2FD%3A%2Fcode%2FAI%2Faideate%2Fmain.py%22%2C%22scheme%22%3A%22file%22%7D%7D)             # Entry point for the FastAPI application
├── [requirements.txt](http://_vscodecontentref_/#%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22d%3A%5C%5Ccode%5C%5CAI%5C%5Caideate%5C%5Crequirements.txt%22%2C%22_sep%22%3A1%2C%22path%22%3A%22%2FD%3A%2Fcode%2FAI%2Faideate%2Frequirements.txt%22%2C%22scheme%22%3A%22file%22%7D%7D)    # Python dependencies
├── src/                # Source code
│   ├── graph/          # Graph-based workflow logic
│   ├── models/         # Database models
│   ├── routes/         # API routes
│   ├── types/          # Type definitions
│   └── utils/          # Utility functions
```

# Prerequisites

- Python 3.12 or higher
- MongoDB instance
- Docker (optional, for containerized deployment)

# Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up the environment variables:
   - Copy `env.sample` to `.env`
   - Update the .env file with your credentials

# Running the Project

## Locally

1. Start the FastAPI application:

```shell
python main.py
```

2. Access the API documentation at
   `http://localhost:8000/docs.`

## Using Docker

1. Build the Docker image:

```shell
docker build -t aidiate .
```

2. Run the container:

```shell
docker run -p 8000:8000 --env-file .env aidiate
```

3. Access the API documentation at `http://localhost:8000/docs`.

# Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

# License

This project is licensed under the MIT License.

# Contact

Author: Lakshya Kumar
Email: lklsquare@gmail.com
