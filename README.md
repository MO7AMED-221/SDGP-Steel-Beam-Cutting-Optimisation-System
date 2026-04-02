# SDGP-Steel-Beam-Cutting-Optimisation-System

Requirements

Make sure you have the following installed:

Node.js (v16 or later recommended)
npm (comes with Node.js)
Python 3
How to Run the Application
Clone the repository
git clone <your-repo-link>
cd <your-project-folder>
Install dependencies
npm install
Run the Electron app
npm start
Notes
Make sure Python is installed and added to your system PATH
The app runs locally (offline)
Upload your CSV file through the dashboard to start processing

Overview: This project is a standalone desktop dashboard designed to minimize material waste in steel beam cutting for ship construction. It uses a mathematical optimization algorithm to calculate the most efficient combination of standard beam sizes and visualize the results through an interactive interface.

Aims: The goal of this system is to reduce trim loss and improve material efficiency by finding the optimal combination of beam lengths (6000mm, 8000mm, 13000mm) for each batch.

Key Features
Functional Features
Automated optimization on data upload
Support for standard beam sizes (6000mm, 8000mm, 13000mm)
Exact mathematical solver (global minimum solution)
Trim loss calculation (mm and %)
Procurement output (beam counts)
Interactive dashboard with charts and beam visualisation
CSV export support
Pattern optimization to reduce machine setup
Non-Functional Features
Standalone desktop app (Electron)
Processes large datasets in under 30 seconds
High accuracy (target >98% efficiency)
Robust CSV validation
User-friendly UI with highlighted high-waste batches
Local data processing for security
System Architecture

The system follows a modular layered architecture:

Input Layer: Handles CSV upload and validation
Algorithm Layer: Python-based optimization engine
IPC Bridge: Connects Electron frontend with backend
Presentation Layer: Dashboard UI and visualisations
Output Layer: Data export and charts
Algorithm

The core algorithm solves a cutting stock problem using an exhaustive search approach to guarantee the global minimum.

Key Points:
Groups data by beam length
Calculates total demand per batch
Searches for the smallest valid beam combination
Minimizes:
Total material used
Number of beams
Uses modular arithmetic for efficiency

Technologies Used
Electron – Desktop application
Python – Optimization algorithm
JavaScript / HTML / CSS – Frontend
CSV Processing – Data handling

Conclusion: This system provides a high-efficiency, secure, and user-friendly solution for industrial beam cutting optimization, achieving near-optimal material utilization while remaining practical for real-world shipyard environments.
