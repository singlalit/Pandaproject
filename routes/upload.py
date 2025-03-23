from flask import Blueprint, request, jsonify
import pandas as pd
import os

upload_blueprint = Blueprint('upload', __name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to process and save sales data
def process_sales_data(file_path):
    df = pd.read_csv(file_path)

    # Save processed data for future use
    processed_path = os.path.join(UPLOAD_FOLDER, "processed_sales_data.csv")
    df.to_csv(processed_path, index=False)
    return df

# Route for file upload
@upload_blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Invalid file format. Please upload a CSV file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    df = process_sales_data(file_path)

    return jsonify({"message": "Data processed successfully!"})

# Function to load processed sales data
def load_processed_data():
    try:
        df = pd.read_csv(os.path.join(UPLOAD_FOLDER, "processed_sales_data.csv"))
        return df
    except FileNotFoundError:
        return None

# Route to fetch sales summary
@upload_blueprint.route('/sales_summary', methods=['GET'])
def sales_summary():
    df = load_processed_data()
    if df is None:
        return jsonify({"error": "No data available"}), 400

    total_sales = df["Revenue"].sum()
    total_orders = df.shape[0]
    top_product = df.groupby("Product")["Revenue"].sum().idxmax()
    top_customer = df.groupby("Customer")["Revenue"].sum().idxmax()

    return jsonify({
        "total_sales": total_sales,
        "total_orders": total_orders,
        "top_product": top_product,
        "top_customer": top_customer
    })
