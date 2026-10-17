from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import TextToSQLAgent
import os

app = FastAPI(
    title="Self-Correcting Text-to-SQL Analytics Agent API",
    description="API for natural language analytics queries backed by LangGraph-style agent workflow and SQLite.",
    version="1.0.0"
)

agent = TextToSQLAgent()

class QueryRequest(BaseModel):
    query: str
    auto_approve: bool = True

class QueryResponse(BaseModel):
    user_query: str
    plan: str
    sql_query: str
    validation_result: bool
    validation_message: str
    execution_success: bool
    columns: list
    results: list
    error_message: str
    retry_count: int
    summary: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Self-Correcting Text-to-SQL Analytics Agent API"}

@app.get("/schema")
def get_schema():
    return agent.schema_info

@app.post("/query", response_model=QueryResponse)
def run_query(request: QueryRequest):
    try:
        state = agent.run(request.query, auto_approve=request.auto_approve)
        return QueryResponse(
            user_query=state.user_query,
            plan=state.plan,
            sql_query=state.sql_query,
            validation_result=state.validation_result,
            validation_message=state.validation_message,
            execution_success=state.execution_success,
            columns=state.columns,
            results=state.results or [],
            error_message=state.error_message,
            retry_count=state.retry_count,
            summary=state.summary
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
