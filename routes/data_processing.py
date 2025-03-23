import pandas as pd
import os

UPLOAD_FOLDER = "uploads"

def process_sales_data(filename):
    """
    Reads the uploaded CSV file, cleans the data, and returns a summary.
    """
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Drop any completely empty columns
        df.dropna(axis=1, how="all", inplace=True)

        # Fill missing values with 0 or 'Unknown' (based on column type)
        df.fillna({"Revenue": 0, "Product": "Unknown", "Customer": "Unknown"}, inplace=True)

        # Convert date column to datetime (assuming it's named 'Date')
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df.dropna(subset=["Date"], inplace=True)  # Drop rows where Date is still NaT

        # Convert numerical columns to proper types
        if "Revenue" in df.columns:
            df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce").fillna(0)

        # Basic summary statistics
        summary = {
            "total_sales": df["Revenue"].sum() if "Revenue" in df.columns else "N/A",
            "total_orders": len(df),
            "top_product": df["Product"].value_counts().idxmax() if "Product" in df.columns else "N/A",
            "top_customer": df["Customer"].value_counts().idxmax() if "Customer" in df.columns else "N/A",
        }

        return {"message": "Data processed successfully!", "summary": summary}

    except Exception as e:
        return {"error": str(e)}
