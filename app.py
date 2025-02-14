from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
app = Flask(__name__)

GEMINI_API_KEY = "AIzaSyAzkLkrRySufY2z14TfqYEF2dNqLdDGF_U"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

def rewrite_headline(headline):
    """Uses Gemini API to rewrite a Fox News headline in MSNBC style."""
    prompt = f"""
Rewrite the following Fox News headline in the style of MSNBC, ensuring that the language aligns with MSNBC’s typical editorial tone. 
- Avoid politically charged or polarizing terms like 'illegal immigrants'; instead, use more neutral or progressive phrasing where appropriate.
- Maintain factual accuracy while adapting the framing, word choice, and emphasis to match MSNBC’s approach.
- If MSNBC would likely cover this topic, provide a rewritten headline in their style.
- If MSNBC is likely not to cover this story at all, respond with: 'NAH, MSNBC ain't covering this. Add (made by Noor Nazir) add the end'

Fox News: "{headline}"

"""


    try:
        response = model.generate_content(prompt)
        return response.text if response else "Failed to generate response"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/rewrite", methods=["POST"])
def rewrite():
    data = request.get_json()
    headline = data.get("headline", "")
    rewritten = rewrite_headline(headline)
    return jsonify({"original": headline, "rewritten": rewritten})

if __name__ == "__main__":
    app.run(debug=True)
