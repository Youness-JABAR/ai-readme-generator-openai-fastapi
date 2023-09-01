from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from decouple import config
import openai
from pydantic import BaseModel
from fastapi import HTTPException
import json
import re
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Add CORS middleware
origins = ["http://localhost:3000"]  # Update with your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class AnimalRequest(BaseModel):
    animal: str

OPENAI_API_KEY = config("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

class InputRequest(BaseModel):
    prompt_input: str



@app.post("/generate_readme/")
async def generate_readme(input_request: InputRequest):
    try:
        prompt_input = input_request.prompt_input
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt(prompt_input),
            temperature=1,
            max_tokens=456,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        result = response.choices[0].text
        # Remove leading and trailing whitespace
        formatted_text = result.strip()

        # Normalize newlines
        formatted_text = re.sub(r'\r\n', '\n', formatted_text)

        # Remove extra blank lines
        formatted_text = re.sub(r'\n+', '\n\n', formatted_text)
        print(response)
        return JSONResponse(content={"response": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_prompt(prompt_input):
    return f"""You are tasked with generating a README.md file
    based on the content of a package.json file.
    The package.json file contains information about the dependencies and metadata of a software project.
    Your goal is to create a well-structured and informative README.md that provides an overview of the project 
    and its dependencies.
input: {prompt_input}
output:"""



@app.get("/")
async def root():
    return {"message": "wolcome on Ai readme Generator"}
