from flask import Blueprint, render_template, send_from_directory

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def homepage():
    """
    Render and return the homepage HTML template.

    Returns:
        str: Rendered HTML for the homepage.
    """
    return render_template('index.html')

@frontend_bp.route('/static/<path:filename>')
def static_files(filename):
    """
    Serve static files from the 'static' directory.

    Args:
        filename (str): The path to the static file to serve.

    Returns:
        Response: The static file response.
    """
    return send_from_directory('static', filename) 