# Import necessary libraries
import pandas as pd                      # For data manipulation and analysis
import matplotlib.pyplot as plt          # For creating plots and charts
from reportlab.lib.pagesizes import letter                  # To set page size
from reportlab.lib import colors                          # For color styling
from reportlab.platypus import (SimpleDocTemplate, Table, 
                                TableStyle, Paragraph, Image)  # For building PDF elements
from reportlab.lib.styles import getSampleStyleSheet       # For text styling

# Load the CSV data into a DataFrame
data = pd.read_csv("data.csv")

# Generate summary statistics (mean, std, min, max, 50%, etc.)
summary_stats = data.describe()

# Define the filename and initialize the PDF document
pdf_filename = "heart_disease_report.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
elements = []  # List to hold PDF elements

# Add a title to the PDF using default style
styles = getSampleStyleSheet()
title = Paragraph("Data Analysis Report", styles["Title"])
elements.append(title)

# Prepare table data with headers
table_data = [["Column", "Mean", "Std Dev", "Min", "Max", "Median"]]

# Fill the table with statistics for each column
for col in summary_stats.columns:
    table_data.append([
        col,
        round(summary_stats.loc["mean", col], 2),   # Mean
        round(summary_stats.loc["std", col], 2),    # Standard deviation
        round(summary_stats.loc["min", col], 2),    # Minimum value
        round(summary_stats.loc["max", col], 2),    # Maximum value
        round(summary_stats.loc["50%", col], 2),    # Median (50th percentile)
    ])

# Create and style the statistics table
table = Table(table_data)

# Apply table styles
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),           # Header background
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),      # Header text color
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),                  # Center all text
    ('GRID', (0, 0), (-1, -1), 1, colors.black),            # Add grid lines
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),        # Header font bold
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),         # Cell background
]))

# Add the table to the list of elements for the PDF
elements.append(table)

# Generate a bar chart for the mean values of the columns
plt.figure(figsize=(8, 4))                                   # Set figure size
summary_stats.loc["mean"].plot(kind="bar", color="skyblue")  # Bar plot of mean values
plt.title("Mean Values of Columns")
plt.xlabel("Columns")
plt.ylabel("Mean Value")
plt.xticks(rotation=45)                                      # Rotate x labels for readability
plt.tight_layout()
plt.savefig("chart.png", bbox_inches="tight")                # Save the plot as an image

# Add the saved chart image to the PDF
elements.append(Image("chart.png", width=400, height=200))   # Adjust size as needed

# Build the final PDF with all the elements
doc.build(elements)

# Confirmation message
print(f"Enhanced report saved as {pdf_filename}")
