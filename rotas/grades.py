@app.post("/grades") # Admin e professor
@app.get("/grades/students/{students_id}") # Admin, aluno e professor
@app.get("/grades/class/{class_id}") # Admin e professor
@app.put("/grades/{grade_id}") # Admin e professor
@app.delete("/grades/{grade_id}") # Admin e professor
 