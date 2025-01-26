from app import app
from flask import render_template, request, send_file
from helpers.processor import startProcess
import io
import base64
import datetime
from helpers.exceptions import *

current_year = datetime.datetime.now().strftime('%Y')
error_code = 0

@app.route('/', methods=["GET", "POST"])
def homepage():
    
    image_src = "static/images/instructions.png"
    
    if request.method == "POST":
        user_input = request.form["user_id"]
        
        grid_size = request.form["grid_size"]
        
        column, line = map(int, grid_size.split(','))

        paste_star = "paste_star" in request.form
        
        try:
            chart_img_grid = startProcess(user_input, column, line, paste_star)
        
        ###Exceptions###
        #1. Invalid input
        except InvalidUserInput as e:
            return render_template("error.html", current_year=current_year, error_code=1)
        #2. Invalid user
        except InvalidUserId as e:
            return render_template("error.html", current_year=current_year, error_code=2)
            
        #3. Not enough registered books
        except NotEnoughRegisteredBooks as e:
            return render_template("error.html", current_year=current_year,total_read_books=e.total_read_books, total_grid_books=e.total_grid_books, error_code=3)
        
        # Generic error
        except Exception as e:
            return render_template("error.html", current_year=current_year, error_code=4)
        
        img_base64 = base64.b64encode(chart_img_grid.getvalue()).decode('utf-8')
        
        current_time_generate = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        
        image_src = f"data:image/png;base64,{img_base64}"

        return render_template("result.html", image_data=img_base64, user_id=user_input, current_time_generate=current_time_generate, current_year=current_year, image_src=image_src)
    
    return render_template("homepage.html", current_year=current_year, image_src=image_src)

@app.route('/sobre')
def about():
    return render_template("about.html", current_year=current_year)

@app.route('/privacidade')
def privacy():
    return render_template("privacy.html", current_year=current_year)

@app.route('/contato')
def contact():
    return render_template("contact.html", current_year=current_year)
