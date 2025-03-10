from pathlib import Path
from sys import argv

data = Path(argv[1]).read_text()
data = data.replace("\n", r"\n").replace('"', r"\"")

request = f"""{{
  "document": {{
    "content": "{data}",
    "type": "PLAIN_TEXT"
  }},
  "encodingType": "UTF8"
}}"""


print(request)
