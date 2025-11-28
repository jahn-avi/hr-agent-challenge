# HR Policy Assistant Agent

## 1. Overview of the Agent

This project implements the **HR Assistant Agent** challenge from Category 1 (People & HR). The agent provides instantaneous, accurate answers to employee questions regarding company policies, leave, and health benefits.

The core functionality is built on a **simplified RAG (Retrieval-Augmented Generation) pattern** where the full HR policy text is injected into the prompt context for the Large Language Model (LLM) for every query. This approach guarantees reliability and avoids complex vector database setup for a small, fixed knowledge base.

## 2. Architecture Diagram (Conceptual)


The system follows a simple linear chain:

1.  **Client (HTML/JS)** sends the user query to the Flask server.
2.  **Flask (`app.py`)** receives the query and combines it with the entire **HR Policy Text**.
3.  **LLM Call:** The combined prompt (Question + Full Policy Context) is sent to the **Gemini API**.
4.  **Response:** Gemini generates a concise, contextual answer based *only* on the provided policy.
5.  The final answer is sent back to the client and displayed in the chat interface.

## 3. Tech Stack & APIs Used

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Agent Core** | Python, Flask | Backend server for handling web requests. |
| **LLM/API** | Google Gemini 2.5 Flash | The generative model used to analyze the policy text and formulate the final answer. |
| **Framework** | LangChain Core | Used primarily for easy integration with the Gemini Chat Model. |
| **Frontend** | HTML, CSS, JavaScript | Provides a modern, responsive chat interface. |
| **Dependencies** | `python-dotenv`, `langchain-google-genai` | Environment configuration and Google API connection. |

## 4. Features & Limitations

### Features
* **Accurate Policy Lookup:** Provides specific details on Casual Leave (12 days), Sick Leave (10 days), Probation (3 months), and Health Insurance ($5,000 cover) directly from the policy.
* **Clean UI/UX:** Features a modern, accessible chat interface built with HTML/CSS.
* **High Reliability:** The simplified, non-RAG architecture avoids common setup errors (like vector store configuration) and eliminates quota errors on the embedding stage.

### Limitations
* **No Chat History:** The agent treats every query as a fresh question and cannot maintain conversational context (e.g., it can't handle follow-up questions like "what about my partner?").
* **Static Knowledge Base:** The HR policy is hardcoded in `app.py`. To update the policy, a developer must modify and restart the application.
* **No Source Tracing:** Since the entire policy is passed as context, the response does not pinpoint the exact line or document section it drew the answer from.

## 5. Setup & Run Instructions

### Prerequisites
* Python 3.8+
* A valid **Google Gemini API Key**.

### Step 1: Clone the Repository and Install Dependencies

```bash
# Clone the repository (Replace with your actual repo link)
git clone [YOUR_REPO_LINK]
cd hr-assistant-agent 

# Install required Python packages
pip install -r requirements.txt