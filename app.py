from flask import Flask, render_template, request, send_file
from helpers.processor import startProcess
import io
import base64
import datetime

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        user_id = request.form["user_id"]
        column = int(request.form["column"])
        line = int(request.form["line"])
        paste_star = "paste_star" in request.form
        
        chart_img_grid = startProcess(user_id, column, line, paste_star)
        
        if chart_img_grid == None or chart_img_grid == ValueError:
            return render_template("erro.html")
        
        img_base64 = base64.b64encode(chart_img_grid.getvalue()).decode('utf-8')
        
        current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        return render_template("homepage.html", image_data=img_base64, user_id=user_id, current_time=current_time)

    return render_template("homepage.html")

@app.route('/image')
def serve_image():
    image_data = request.args.get("image_data")
    if image_data:
        chart_img = io.BytesIO(image_data.encode('utf-8'))
        chart_img.seek(0)
        
        return send_file(chart_img, mimetype='image/png')
    return "No image data found", 400

@app.route('/sobre')
def about():
    return render_template("about.html")

@app.route('/privacidade')
def privacy():
    return render_template("privacy.html")

@app.route('/contato')
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)