import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# --- UPDATED IMPORTS TO FIX ERRORS ---
# New location for text splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Core LangChain components (Make sure you ran: pip install langchain)

# Google Gemini & FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# --- 1. LOAD ENVIRONMENT VARIABLES ---
load_dotenv()

# Verify Key exists
if not os.getenv("GOOGLE_API_KEY"):
    print("CRITICAL ERROR: GOOGLE_API_KEY not found. Please check your .env file.")

app = Flask(__name__)

# --- 2. CREATE DUMMY HR DATA (The Knowledge Base) ---
# [cite_start]This matches the HR Assistant Agent requirement [cite: 13]
hr_policy_text = """
*** COMPANY HR POLICY MANUAL ***

1. LEAVE POLICY
   - Casual Leave (CL): Employees are entitled to 12 days of CL per year.
   - Sick Leave (SL): 10 days of paid sick leave per year. Medical certificate required for >2 days.
   - Privilege Leave (PL): 15 days per year, applicable after completing probation.
   - Maternity Leave: 26 weeks of paid leave for expecting mothers.
   - Paternity Leave: 1 week of paid leave for new fathers.

2. WORKING HOURS
   - Standard hours are 9:00 AM to 6:00 PM, Monday to Friday.
   - Flexible timing is allowed with manager approval (core hours 11 AM - 4 PM).
   - Lunch break is 1 hour, typically between 1:00 PM and 2:00 PM.

3. HEALTH BENEFITS
   - All employees are covered under Group Health Insurance up to $5,000.
   - Gym reimbursement of $30/month is available upon submission of bills.
   - Annual health checkup is sponsored by the company once per year.

4. REMOTE WORK
   - Employees are allowed 2 days of Work From Home (WFH) per week.
   - Full remote options depend on the project requirements and manager approval.

5. PROBATION & NOTICE PERIOD
   - Standard probation period is 3 months. 
   - Notice period during probation is 15 days.
   - Notice period after confirmation is 60 days.
"""

# --- 3. INITIALIZE RAG PIPELINE ---
print("Initializing Vector DB...")

try:
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = [Document(page_content=x) for x in text_splitter.split_text(hr_policy_text)]

    # Create Embeddings & Vector DB (FAISS)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_db = FAISS.from_documents(docs, embeddings)

    # Setup Gemini LLM
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)

    # Create the QA Chain
    prompt_template = """
    You are a helpful HR Assistant. Use the following context from the company policy to answer the employee's question.
    If the answer is not in the context, say "I'm sorry, I cannot find that specific information in the HR policy."

    Context: {context}

    Question: {question}

    Helpful Answer:
    """
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 2}),
        chain_type_kwargs={"prompt": PROMPT}
    )
    print("Agent Ready!")

except Exception as e:
    print(f"Error initializing AI: {e}")
    print("Make sure your API Key is correct in .env and you have internet access.")

# --- 4. FLASK ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message')
    
    if not user_message:
        return jsonify({"response": "Please type a question."})

    try:
        # Run the LangChain agent
        response = qa_chain.run(user_message)
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error during query: {e}")
        return jsonify({"response": "Sorry, I encountered an error processing your request."})

if __name__ == '__main__':
    app.run(debug=True, port=5000)