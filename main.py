import os
from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types
from openai import OpenAI
from dotenv import load_dotenv

# এনভায়রনমেন্ট ভেরিয়েবল লোড করা
load_dotenv()

app = Flask(__name__)

# ১. Google GenAI ক্লায়েন্ট সেটআপ
gemini_client = genai.Client()

# ২. OpenAI ক্লায়েন্ট সেটআপ
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=openai_api_key) if openai_api_key else None

# সিস্টেম ইন্সট্রাকশন
SYSTEM_INSTRUCTION = (
    "You are a helpful AI assistant. If anyone asks who made, created, built, or developed you in any phrasing, "
    "you must always strictly answer that it was made by MD. JAKARIA NAIM."
)

# Gemini সিস্টেম কনফিগারেশন
gemini_config = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        user_input = data.get("message")
        
        if not user_input:
            return jsonify({"error": "Message is required"}), 400

        # ক্রিয়েটর সম্পর্কিত যেকোনো প্রশ্নের সরাসরি ও নিশ্চিত উত্তর
        normalized = user_input.lower().strip().rstrip('?.!,')
        who_words = ["who", "whom", "whose", "কে", "কার"]
        maker_verbs = ["made", "created", "built", "developed", "coded", "programmed", "authored", "বানিয়েছে", "তৈরি করেছে", "বানাইছে"]
        creator_nouns = ["creator", "developer", "author", "maker", "founder", "owner", "নির্মাতা", "প্রোগ্রামার", "ডেভেলপার"]

        is_creator_query = (
            (any(w in normalized for w in who_words) and (any(v in normalized for v in maker_verbs) or any(n in normalized for n in creator_nouns)))
            or any(phrase in normalized for phrase in [
                "who made", "who created", "who built", "who developed", "who coded", "who programmed",
                "made by who", "created by who", "built by who", "developed by who"
            ])
        )

        if is_creator_query:
            return jsonify({"response": "It was made by MD. JAKARIA NAIM."})

        response_text = None

        # ১. প্রথমে Gemini API ব্যবহার করা (Primary API)
        gemini_candidate_models = ['gemini-3.5-flash-lite', 'gemini-3.1-flash-lite', 'gemini-3.8-flash']
        for model_name in gemini_candidate_models:
            try:
                gemini_res = gemini_client.models.generate_content(
                    model=model_name,
                    contents=user_input,
                    config=gemini_config
                )
                if gemini_res and gemini_res.text:
                    response_text = gemini_res.text
                    print(f"[Gemini API] Successfully generated response with model: {model_name}")
                    break
            except Exception as gemini_err:
                err_summary = str(gemini_err).splitlines()[0] if str(gemini_err) else "Error"
                print(f"[Gemini API] Error on {model_name}: {err_summary[:80]}")
                continue

        # ২. যদি Gemini API-এর লিমিট শেষ বা কোনো এরর হয় -> স্বয়ংক্রিয়ভাবে OpenAI API কাজ করবে (Fallback API)
        if not response_text:
            print("[Fallback Activated] Gemini limit reached or unavailable. Switching to OpenAI API...")
            
            # রানটাইমে .env রি-রিড করা যাতে ইউজার কি বসালে সাথে সাথে পায়
            load_dotenv(override=True)
            active_openai_key = os.getenv("OPENAI_API_KEY")

            if active_openai_key and active_openai_key.strip():
                try:
                    active_client = OpenAI(api_key=active_openai_key.strip())
                    for openai_model in ['gpt-4o-mini', 'gpt-4o', 'gpt-3.5-turbo']:
                        try:
                            completion = active_client.chat.completions.create(
                                model=openai_model,
                                messages=[
                                    {"role": "system", "content": SYSTEM_INSTRUCTION},
                                    {"role": "user", "content": user_input}
                                ]
                            )
                            if completion.choices and completion.choices[0].message.content:
                                response_text = completion.choices[0].message.content
                                print(f"[OpenAI API] Successfully generated response with model: {openai_model}")
                                break
                        except Exception as oai_err:
                            err_summary = str(oai_err).splitlines()[0] if str(oai_err) else "Error"
                            print(f"[OpenAI API] Error on {openai_model}: {err_summary[:80]}")
                            continue
                except Exception as client_err:
                    print(f"[OpenAI Client] Initialization error: {client_err}")
            else:
                print("[OpenAI Warning] OPENAI_API_KEY is not configured in .env file.")

        # ৩. কোনো কারণে যদি উভয় API রেসপন্স দিতে ব্যর্থ হয়
        if not response_text:
            if not os.getenv("OPENAI_API_KEY"):
                return jsonify({
                    "error": "Gemini limit exceeded. Please add your OPENAI_API_KEY into the .env file so OpenAI can take over as fallback."
                }), 503
            return jsonify({
                "error": "Both Gemini and OpenAI services are temporarily busy. Please try again in a moment."
            }), 503

        return jsonify({"response": response_text})

    except Exception as e:
        print("Error in /chat:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)