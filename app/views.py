import json
import os
import requests
from flask import render_template, redirect, request, send_file, render_template_string
from werkzeug.utils import secure_filename
from app import app
from timeit import default_timer as timer

# Stores all the post transaction in the node
request_tx = []
# store filename
files = {}
# destiantion for upload files
UPLOAD_FOLDER = "static/Uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# store  address
ADDR = "http://127.0.0.1:8800"


# create a list of requests that peers has sent to upload files
def get_tx_req():
    global request_tx
    chain_addr = "{0}/chain".format(ADDR)
    resp = requests.get(chain_addr)
    if resp.status_code == 200:
        content = []
        chain = json.loads(resp.content.decode())
        for block in chain["chain"]:
            for trans in block["transactions"]:
                trans["index"] = block["index"]
                trans["hash"] = block["prev_hash"]
                content.append(trans)
        request_tx = sorted(content, key=lambda k: k["hash"], reverse=True)


# Loads and runs the home page
@app.route("/")
def index():
    get_tx_req()
    return render_template("index.html", title="FileStorage",
                           subtitle="A Decentralized Network for File Storage/Sharing", node_address=ADDR,
                           request_tx=request_tx)


@app.route("/submit", methods=["POST"])
# When new transaction is created it is processed and added to transaction
def submit():
    start = timer()
    user = request.form["user"]
    up_file = request.files["v_file"]

    # save the uploaded file in destination
    upload_dir = "/code/app/static/Uploads/"
    os.makedirs(upload_dir, exist_ok=True)

    # Construct absolute file path
    up_file_path = os.path.join(upload_dir, secure_filename(up_file.filename))

    # Save the uploaded file
    up_file.save(up_file_path)

    # Add the file to the list to create a download link
    files[up_file.filename] = up_file_path

    # Determine the size of the file uploaded in bytes
    file_states = os.stat(up_file_path).st_size
    # create a transaction object
    post_object = {
        "user": user,  # user name
        "v_file": up_file.filename,  # filename
        "file_data": str(up_file.stream.read()),  # file data
        "file_size": file_states  # file size
    }

    # Submit a new transaction
    address = "{0}/new_transaction".format(ADDR)
    requests.post(address, json=post_object)
    end = timer()
    print(end - start)
    return redirect("/")



# Search route
@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "").lower()

    # Filter transactions based on the search query
    search_results = [tx for tx in request_tx if query in tx["user"].lower() or query in tx["v_file"].lower()]

    return render_template_string("""
        {% extends "base.html" %} 
        {% block content %}
            <!-- Add the search results section in your HTML here -->
            <div class="col-sm-4">
                <h2 class="text-center alert alert-primary">Search Results</h2>
                {% if search_results %}
                    {% for result in search_results %}
                        <div class="post_box">
                            <!-- Display search results here -->
                            <!-- Customize the display based on your requirements -->
                            <p>{{ result.user }} - {{ result.v_file }}</p>
                        </div>
                    {% endfor %}
                {% else %}
                    <p>No results found.</p>
                {% endif %}
            </div>
        {% endblock %}
    """)


# creates a download link for the file
@app.route("/submit/<string:variable>", methods=["GET"])
def download_file(variable):
    p = files[variable]
    return send_file(p, as_attachment=True)
