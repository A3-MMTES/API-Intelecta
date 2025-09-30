@app.get("/teachers") # admin
@app.post("/teachers") # admin
@app.get("/teachers/{id}") # admin e professor
@app.put("/teachers/{id}") # admin
@app.delete("/teachers/{id}") # admin
