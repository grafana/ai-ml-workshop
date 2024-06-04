import requests
from ast import literal_eval

# Your OpenAI API Key
API_KEY = 'openai-api-key'

PROMPT = """
You are given a Named entity recognition problem.

You are given list of titles of declared incidents.

We want to extract two key information from the titles if they exist

1. The service affected (SVC)
2. The environment affected (ENV)

The text will represented as a list of words.

You will label the first word of the relevant entity with: B-SVC or B-ENV

Any subsequent words will be labeled I-SVC or I-ENV

Unrelated words will be labeled 'O' by default.

Example:
```python
# proxy gateway is down in prod-us-east-3
[
    [
        "B-SVC",  # proxy
        "I-SVC",  # gateway
        "O",  # is
        "O",  # down
        "O",  # in
        "B-ENV",  # prod-us-east-3
    ],
    ...
]
```

only return the list, do not explain or provide any other information.
```python
"""

def gpt_ner(data: str, model: str = 'gpt-3.5-turbo') -> list[list[str]]:
    url = 'https://api.openai.com/v1/chat/completions'
    # Headers including the Authorization token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    data = {
        "model": model,
        "messages": [
            { "role": "system", "content": [{ "type": "text", "text": PROMPT, }] },
            { "role": "user", "content": [{ "type": "text", "text": data, }] },
        ],
        "temperature": 0.5,
        "max_tokens": 1024,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return literal_eval(response.json()['choices'][0]['message']['content'])
    else:
        return []
