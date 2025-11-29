# HR Policy Assistant Agent (Enhanced)

## 1. Overview of the Agent

This project implements the **HR Assistant Agent** using a simplified RAG (Retrieval-Augmented Generation) pattern. The agent provides instantaneous, accurate answers to employee questions regarding:

* **Company Policies** (e.g., Working Hours, Remote Work, Probation).
* **Leave and Health Benefits**.
* **Payroll and Compensation** (e.g., PF contribution, tax queries, salary structure).

The core policy text is injected into the prompt context for the Large Language Model (LLM) for every query, ensuring a high degree of reliability for the fixed knowledge base.

***

## 2. Architecture Diagram (Conceptual)

The system follows a simple linear chain:

1.  **Client (HTML/JS)** sends the user query to the Flask server.
2.  **Flask (`app.py`)** receives the query and combines it with the entire **HR Policy Text**.
3.  **LLM Call:** The combined prompt (Question + Full Policy Context) is sent to the **Gemini API**.
4.  **Response:** Gemini generates a concise, contextual answer based *only* on the provided policy.
5.  The final answer is sent back to the client, displayed with enhanced formatting, and read aloud via Text-to-Speech (TTS).

***

## 3. Tech Stack & APIs Used

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Agent Core** | Python, Flask | Backend server for handling web requests. |
| **LLM/API** | Google Gemini 2.5 Flash | The generative model used to analyze the policy text and formulate the final answer. |
| **Framework** | LangChain Core | Used primarily for easy integration with the Gemini Chat Model. |
| **Frontend** | HTML, CSS, JavaScript (Web Speech API) | Provides a modern, responsive chat interface with **Text-to-Speech** capability. |
| **Dependencies** | `python-dotenv`, `langchain-google-genai` | Environment configuration and Google API connection. |

***

## 4. Features & Limitations

### Features
* **Expanded Knowledge:** Now includes a comprehensive **Payroll & Compensation** section, answering common queries about PF, tax deductions, and salary structure.
* **Voice Output (Text-to-Speech):** Utilizes the browser's native **Web Speech API** to automatically read the bot's response aloud, enhancing accessibility.
* **Enhanced UI/UX:** Features a modern, responsive chat interface with custom JavaScript to properly render **Markdown formatting** (e.g., bold text, bulleted lists) from the LLM, making answers easier to read.
* **Accurate Policy Lookup:** Provides specific details on Casual Leave (12 days), Sick Leave (10 days), Probation (3 months), and Health Insurance ($5,000 cover).

### Limitations
* **No Chat History:** The agent remains stateless and treats every query as a fresh question; it cannot handle follow-up questions that rely on previous turns.
* **Static Knowledge Base:** The HR policy is hardcoded in `app.py`. To update the policy, a developer must modify and restart the application.
* **No Source Tracing:** Since the entire policy is passed as context, the response does not pinpoint the exact line or document section it drew the answer from.

***

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