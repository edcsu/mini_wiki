from app import app

@app.route("/")
@app.route("/index")
def add_document():
  return "<p>Hello documents</p>"
