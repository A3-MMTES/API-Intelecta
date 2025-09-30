
@app.get("/reports/students/{students_id}") # Admin, aluno e professor
@app.get("/reports/class/{class_id}") # Admin e professor

@app.get("/dashboard/admin") # Admin
@app.get("/dashboard/teachers") # Professores
@app.get("/dashboard/students") # Alunos
