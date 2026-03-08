import os, requests, json
def get_daily_concept():
    api_key = os.getenv('AI_API_KEY')
    url = "https://openrouter.ai/api/v1/chat/completions"
    prompt = "Generate 20 unique color palettes (4 hex codes each) and 20 random integer seeds. Output strictly JSON: {'palettes': [[...], ...], 'seeds': [...]}"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"model": "google/gemini-2.0-flash-001", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data)
    result = response.json()['choices'][0]['message']['content']
    clean_json = result.replace('\`\`\`json', '').replace('\`\`\`', '').strip()
    with open('daily_params.json', 'w') as f:
        f.write(clean_json)
if __name__ == "__main__":
    get_daily_concept()
