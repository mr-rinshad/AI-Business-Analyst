from decimal import Decimal
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from analysis.answer_generator import generate_answer
from analysis.business_analysis import (
    extract_month,
    investigate_revenue_change,
    validate_revenue_direction,
)
from analysis.intent_detector import detect_intent
from analysis.metric_detector import detect_metric
from analysis.dimension_detector import detect_dimension
from analysis.router import route_analysis
from analysis.investigation_answer import generate_investigation_answer
from analysis.sql_executor import execute_sql
from analysis.sql_generator import generate_sql
from analysis.visualization_engine import visualize_result

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"

app = FastAPI(
    title="AI Business Analyst API",
    description="AI-powered business analytics assistant",
    version="1.0.0",
)


# --------------------------------
# CORS Configuration
# --------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------
# Serve Output Files
# --------------------------------

app.mount(
    "/outputs",
    StaticFiles(directory=str(OUTPUTS_DIR)),
    name="outputs",
)


class QuestionRequest(BaseModel):
    question: str


# --------------------------------
# Convert NumPy/Pandas values
# into JSON-safe Python values
# --------------------------------

def convert_to_json_safe(data):
    if hasattr(data, "to_dict"):
        return convert_to_json_safe(data.to_dict(orient="records"))

    if isinstance(data, dict):
        return {key: convert_to_json_safe(value) for key, value in data.items()}

    if isinstance(data, list):
        return [convert_to_json_safe(value) for value in data]

    if isinstance(data, Decimal):
        return float(data)

    if hasattr(data, "item"):
        return data.item()

    return data


# --------------------------------
# Root
# --------------------------------

@app.get("/")
def root():
    return {"message": "AI Business Analyst API is running"}


# --------------------------------
# Ask Business Question
# --------------------------------

@app.post("/ask")
def ask_business_question(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:
        # --------------------------------
        # Detect Intent
        # --------------------------------
        intent = detect_intent(question)

        metric = detect_metric(question)

        dimension = detect_dimension(question)

        route = route_analysis(intent,metric,dimension)
        # --------------------------------
        # INVESTIGATION
        # --------------------------------
        if intent == "investigation":
            current_month = extract_month(question)

            if current_month is None:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Please specify a month, "
                        "for example: "
                        "'Why did revenue change in March?'"
                    ),
                )

            previous_month = 12 if current_month == 1 else current_month - 1

            investigation = investigate_revenue_change(
                previous_month,
                current_month,
            )

            direction_check = validate_revenue_direction(
                question,
                investigation["comparison"],
            )

            answer = generate_investigation_answer(
                question,
                investigation,
                direction_check,
            )

            return {
                "question": question,
                "intent": intent,
                "metric": metric,
                "dimension": dimension,
                "route": route,
                "answer": answer,
                "analysis": convert_to_json_safe(investigation),
            }

        # --------------------------------
        # NORMAL QUERY
        # --------------------------------
        sql = generate_sql(question)
        result = execute_sql(sql)
        answer = generate_answer(question, sql, result)
        chart = visualize_result(question, result)

        chart_url = None
        if chart:
            chart_url = "http://127.0.0.1:8000/" + chart.replace("\\", "/")

        data = convert_to_json_safe(result)

        return {
            "question": question,
            "intent": intent,
            "metric": metric,
            "dimension": dimension,
            "route": route,
            "sql": sql,
            "data": data,
            "answer": answer,
            "chart": chart_url,
        }

    except HTTPException:
        raise

    except Exception as error:
        print("ERROR:", error)
        raise HTTPException(
            status_code=500,
            detail="Unable to process the business question.",
        )