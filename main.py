from fastapi import FastAPI
from pydantic import BaseModel
import sympy as sp

app = FastAPI(title="AI Math Solver API")

# Model untuk input
class MathInput(BaseModel):
    expression: str
    operation: str   # "diff", "integrate", "simplify", "expand"

x = sp.Symbol('x')  # variabel default, bisa diperluas nanti

def step_by_step_diff(expr):
    steps = []
    expr_simplified = sp.simplify(expr)
    steps.append(f"Fungsi awal: {expr}")
    steps.append(f"Sederhanakan: {expr_simplified}")
    
    derivative = sp.diff(expr_simplified, x)
    steps.append(f"Turunan terhadap x: {derivative}")
    return steps, derivative

def step_by_step_integrate(expr):
    steps = []
    steps.append(f"Fungsi awal: {expr}")
    result = sp.integrate(expr, x)
    steps.append(f"Hasil integral: {result} + C")
    return steps, result

def step_by_step_simplify(expr):
    steps = []
    steps.append(f"Ekspresi awal: {expr}")
    simp = sp.simplify(expr)
    steps.append(f"Hasil simplifikasi: {simp}")
    return steps, simp

def step_by_step_expand(expr):
    steps = []
    steps.append(f"Ekspresi awal: {expr}")
    expd = sp.expand(expr)
    steps.append(f"Hasil ekspansi: {expd}")
    return steps, expd


@app.post("/solve")
async def solve_math(data: MathInput):
    expr = sp.sympify(data.expression)
    steps, result = [], None

    if data.operation == "diff":
        steps, result = step_by_step_diff(expr)
    elif data.operation == "integrate":
        steps, result = step_by_step_integrate(expr)
    elif data.operation == "simplify":
        steps, result = step_by_step_simplify(expr)
    elif data.operation == "expand":
        steps, result = step_by_step_expand(expr)
    else:
        return {"error": "Operasi tidak dikenal"}

    return {
        "input": data.expression,
        "operation": data.operation,
        "steps": steps,
        "result": str(result)
    }
