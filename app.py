import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load Env
load_dotenv()
if not os.getenv("GOOGLE_API_KEY"):
    print("CRITICAL ERROR: GOOGLE_API_KEY not found in .env file.")

app = Flask(__name__)

# --- THE HR DATA (Context) ---
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

# --- SETUP THE AI ---
# FINAL CHANGE: Using the most compatible and modern model alias.
chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message')
    
    if not user_message:
        return jsonify({"response": "Please type a question."})

    try:
        # Create a simple prompt with the policy + user question
        prompt = f"""
        You are a helpful HR Assistant. Use the policy below to answer the question.
        
        --- HR POLICY ---
        {hr_policy_text}
        -----------------
        
        User Question: {user_message}
        
        Answer:
        """
        
        # Send to Gemini
        response = chat_model.invoke(prompt)
        return jsonify({"response": response.content})

    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"response": f"Sorry, I crashed: {str(e)}"})

if __name__ == '__main__':
    print("Starting Simple HR Agent (Gemini 2.5 Flash)...")
    app.run(debug=True, port=5000)