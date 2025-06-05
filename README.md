# Interactive Media Intelligence Dashboard

This Streamlit web application provides a powerful and intuitive dashboard for analyzing media intelligence data. It allows users to upload a CSV file, automatically cleans and processes the data, and then visualizes key metrics through interactive charts. What sets this dashboard apart is its integration with AI capabilities, enabling dynamic generation of campaign recommendations and insightful summaries for each chart.

---

## ✨ Features

* **CSV Data Upload:** Easily upload your media intelligence data in a CSV format.
* **Automated Data Cleaning:** The app handles data cleaning, including date conversion, missing value imputation for engagements, and column name normalization.
* **Interactive Data Visualizations:** Explore your data through 5 interactive Plotly charts:
    * Sentiment Breakdown (Pie Chart)
    * Engagement Trend over Time (Line Chart)
    * Platform Engagements (Bar Chart)
    * Media Type Mix (Pie Chart)
    * Top 5 Locations by Engagement (Bar Chart)
* **AI-Powered Insights (OpenRouter Integration):**
    * **Custom API Key Input:** Users can input their OpenRouter API key directly within the app.
    * **Model Selection:** Choose from recommended free AI models on OpenRouter for analysis.
    * **Overall Campaign Recommendation:** Get a comprehensive AI-generated recommendation for your media campaign, detailing "What's Working" and "What Needs to be Improved."
    * **Chart-Specific Insights:** Generate top 3 insights for each individual chart based on its data.
* **Apple UI Inspired Design:** A clean, modern, and aesthetically pleasing user interface.

---

## 💻 Tech Stack

This dashboard is built using a combination of powerful and modern technologies to provide a seamless and interactive experience:

* **Python:** The primary programming language used for all backend logic, data processing, and AI integration.
* **Streamlit:** An open-source app framework for Machine Learning and Data Science teams. It's used to build the interactive web application with a simple Python script, enabling rapid prototyping and deployment.
* **Pandas:** A fundamental data manipulation and analysis library for Python. It's used for efficient CSV parsing, data cleaning (e.g., date conversion, handling missing values, column normalization), and data aggregation.
* **Plotly:** A powerful graphing library that allows for creating interactive, publication-quality graphs. It's integrated with Streamlit to render dynamic and responsive data visualizations.
* **OpenAI SDK:** The official Python library for interacting with OpenAI-compatible APIs. It's used here to send requests to the OpenRouter.ai platform for AI model inference.
* **OpenRouter.ai:** A unified API for various large language models. It serves as the platform through which the application accesses different AI models for generating insights and recommendations.
* **HTML/CSS (via Streamlit Markdown):** Custom CSS, inspired by Apple's design principles, is injected into the Streamlit application using Markdown to achieve the clean, modern user interface.

---

## 🧠 AI Capabilities & Recommended Models

This dashboard leverages the power of Large Language Models (LLMs) via the [OpenRouter.ai API](https://openrouter.ai/). By providing your OpenRouter API key, you can unlock AI-driven analyses.

We recommend using the following free models from OpenRouter for optimal performance and cost-effectiveness:

* **Mistral 7B Instruct:** `mistralai/mistral-7b-instruct`
* **Nous Hermes 2 Mixtral 8x7B SFT:** `nousresearch/nous-hermes-2-mixtral-8x7b-sft`

These models are selected for their balance of performance and accessibility on the OpenRouter platform.

---

## 🚀 Installation

To get started with the Media Intelligence Dashboard, follow these steps:

1.  **Clone the repository (if applicable):**
    ```bash
    # If this project were in a Git repository
    # git clone <repository-url>
    # cd media-intelligence-dashboard
    ```
    (For this example, assume you have the `app.py` and `requirements.txt` files in a directory.)

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    # venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**
    Navigate to the directory containing `requirements.txt` and run:
    ```bash
    pip install -r requirements.txt
    ```

---

## 🖥️ Usage

1.  **Run the Streamlit application:**
    From your terminal in the project directory, execute:
    ```bash
    streamlit run app.py
    ```
    This will open the dashboard in your default web browser.

2.  **Upload your CSV file:**
    Click the "Select CSV File" button in Section 1 and choose your media intelligence data. Ensure your CSV file has the following columns: `Date`, `Platform`, `Sentiment`, `Location`, `Engagements`, `Media Type`.

3.  **Review Data Cleaning Status:**
    Section 2 will indicate if the data cleaning was successful.

4.  **Configure AI Capabilities:**
    In Section 4, enter your **OpenRouter API Key** and select your preferred AI model from the dropdown.

5.  **Generate Insights & Recommendations:**
    * Click the "Generate Campaign Recommendation" button to get an overall strategic summary.
    * For each chart, click the "Generate Insights for..." button to get specific AI-driven insights for that visualization.

---

## 📊 CSV File Format

Your CSV file *must* contain the following columns (case-insensitive, spaces are handled during cleaning):

* `Date`: Date of the media mention (e.g., `YYYY-MM-DD`).
* `Platform`: The social media or news platform (e.g., `Twitter`, `Facebook`, `News Site`).
* `Sentiment`: The sentiment of the mention (e.g., `Positive`, `Negative`, `Neutral`).
* `Location`: The geographical location associated with the mention.
* `Engagements`: The number of engagements (likes, shares, comments, etc.). Missing values will be filled with `0`.
* `Media Type`: The type of media content (e.g., `Text`, `Image`, `Video`).
