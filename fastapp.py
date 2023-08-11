from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import StreamingResponse
import openai
import os
import sys
import time
import asyncio

# Getting OpenAI API Key
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_KEY = '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'
if not len(OPENAI_API_KEY):
    print("Please set OPENAI_API_KEY environment variable. Exiting.")
    sys.exit(1)

openai.api_key = OPENAI_API_KEY

# Parameters for OpenAI
openai_model = "gpt-3.5-turbo"
max_responses = 1
temperature = 0.7
max_tokens = 512

# Defining the FastAPI app and metadata
app = FastAPI(
    title="Streaming API",
    description="""### API specifications\n
To test out the Streaming API , fire a sample query, then use the Curl command in your terminal to see it stream in real time\n
This doc does not support streaming outputs, but curl does.
              """,
    version=1.0,
)

# Defining error in case of 503 from OpenAI
error503 = "OpenAI server is busy, try again later"


def get_response_openai(prompt):
    try:
        prompt = prompt
        response = openai.ChatCompletion.create(
            model=openai_model,
            temperature=temperature,
            max_tokens=max_tokens,
            n=max_responses,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            messages=[
                {"role": "system", "content": "You are an expert in insurance doamin. Answer the question the user enters."},
                {"role": "user", "content": prompt},
            ],
            stream=True,
        )
    except Exception as e:
        print("Error in creating campaigns from openAI:", str(e))
        raise HTTPException(503, error503)
    try:
        for chunk in response:
            current_content = chunk["choices"][0]["delta"].get("content", "")
            yield current_content
    except Exception as e:
        print("OpenAI Response (Streaming) Error: " + str(e))
        raise HTTPException(503, error503)


@app.get(
    "/chat/",
    tags=["APIs"],
    response_model=str,
    responses={503: {"detail": error503}},
)
def chat(prompt: str = Query(..., max_length=100)):
    return StreamingResponse(get_response_openai(prompt), media_type="text/event-stream")


def get_text_stream(text_file_path):
    with open(text_file_path, "r") as file:
        for line in file:
            for word in line.split():
                yield word
                time.sleep(0.1)


@app.get("/txtstream/")
async def txtstream():
    return StreamingResponse(get_text_stream('sample_file.txt'), media_type="text/event-stream")

outputData = [{'question':'what is insurance?',
               'answer':'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'}]


def get_prompt_answer(prompt):
    for entry in outputData:
        if entry['question'] == prompt:
            for word in entry['answer'].split():
                yield f"{word} "
                time.sleep(0.1)


@app.get("/prompt_answer/",
         tags=["APIs"],
         response_model=str)
async def prompt_answer(prompt: str = Query(..., max_length=100)):
    print(prompt)
    return StreamingResponse(get_prompt_answer(prompt), media_type="text/event-stream")
