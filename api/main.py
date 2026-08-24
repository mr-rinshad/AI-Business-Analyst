from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from analysis.sql_generator import generate_sql
from analysis.sql_executor import execute_sql
from analysis.answer_generator import generate_answer
from analysis.visualization_engine import visualize_result
from analysis.intent_detector import detect_intent
from analysis.business_analysis import investigate_revenue_drop
from analysis.investigation_answer import (
    generate_investigation_answer
)


app = FastAPI(
    title="AI Business Analyst API",
    description="AI-powered business analytics assistant",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class QuestionRequest(BaseModel):

    question: str


# --------------------------------
# Convert NumPy/Pandas values
# into JSON-safe Python values
# --------------------------------

def convert_to_json_safe(data):

    if hasattr(data, "to_dict"):

        return convert_to_json_safe(
            data.to_dict(orient="records")
        )

    if isinstance(data, dict):

        return {
            key: convert_to_json_safe(value)
            for key, value in data.items()
        }

    if isinstance(data, list):

        return [
            convert_to_json_safe(value)
            for value in data
        ]

    if hasattr(data, "item"):

        return data.item()

    return data


@app.get("/")
def root():

    return {
        "message": "AI Business Analyst API is running"
    }


@app.post("/ask")
def ask_business_question(
    request: QuestionRequest
):

    question = request.question.strip()

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        intent = detect_intent(question)

        # --------------------------------
        # INVESTIGATION
        # --------------------------------

        if intent == "investigation":

            investigation = investigate_revenue_drop(
                1,
                2
            )

            answer = generate_investigation_answer(
                question,
                investigation
            )

            return {
                "question": question,
                "intent": intent,
                "answer": answer,
                "analysis": convert_to_json_safe(
                    investigation
                )
            }

        # --------------------------------
        # NORMAL QUERY
        # --------------------------------

        sql = generate_sql(question)

        result = execute_sql(sql)

        answer = generate_answer(
            question,
            sql,
            result
        )

        chart = visualize_result(
            question,
            result
        )

        data = convert_to_json_safe(
            result
        )

        return {
            "question": question,
            "intent": intent,
            "sql": sql,
            "data": data,
            "answer": answer,
            "chart": chart
        }

    except Exception as error:

        print("ERROR:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to process the business question."
        )