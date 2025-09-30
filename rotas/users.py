@app.get("/users/me")
@app.get("/users") # admin
@app.get("/users/{id}") # admin
@app.put("/users/{id}") # admin e usuário 
@app.delete("/users/{id}") # admin