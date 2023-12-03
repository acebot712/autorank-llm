import llm

model = llm.get_model("gpt-3.5-turbo")
model.key = 'YOUR_API_KEY_HERE'
response = model.prompt("Five surprising names for a pet pelican")
print(response.text())