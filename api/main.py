from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles


BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUTS_DIR = BASE_DIR / "outputs"


from analysis.sql_generator import generate_sql
from analysis.sql_executor import execute_sql
from analysis.answer_generator import generate_answer
from analysis.visualization_engine import visualize_result
from analysis.intent_detector import detect_intent
from analysis.business_analysis import investigate_revenue_drop
from analysis.investigation_answer import (
    generate_investigation_answer
)
from analysis.month_detector import (
    get_investigation_months
)


app = FastAPI(
    title="AI Business Analyst API",
    description="AI-powered business analytics assistant",
    version="1.0.0"
)


# --------------------------------
# CORS Configuration
# --------------------------------

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# --------------------------------
# Serve Output Files
# --------------------------------

app.mount(
    "/outputs",
    StaticFiles(directory=str(OUTPUTS_DIR)),
    name="outputs"
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


# --------------------------------
# Root
# --------------------------------

@app.get("/")
def root():

    return {
        "message": "AI Business Analyst API is running"
    }


# --------------------------------
# Ask Business Question
# --------------------------------

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

        # --------------------------------
        # Detect Intent
        # --------------------------------

        intent = detect_intent(question)


        # --------------------------------
        # INVESTIGATION
        # --------------------------------

        if intent == "investigation":

            previous_month, current_month = (
                get_investigation_months(question)
            )


            if current_month is None:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Please specify the month you want "
                        "to investigate. Example: Why did "
                        "revenue drop in February?"
                    )
                )


            if previous_month is None:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "January investigation currently "
                        "requires previous-year data. "
                        "Please choose February or a later month."
                    )
                )


            investigation = investigate_revenue_drop(
                previous_month,
                current_month
            )


            answer = generate_investigation_answer(
                question,
                investigation
            )


            return {

                "question": question,

                "intent": intent,

                "comparison": {
                    "previous_month": previous_month,
                    "current_month": current_month
                },

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


        chart_url = None

        if chart:

            chart_url = (
                "http://127.0.0.1:8000/"
                + chart.replace("\\", "/")
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

            "chart": chart_url

        }


    except HTTPException:

        raise


    except Exception as error:

        print("ERROR:", error)

        raise HTTPException(

            status_code=500,

            detail="Unable to process the business question."

        )