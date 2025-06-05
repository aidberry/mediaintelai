import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import openai # Import the openai library

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="Interactive Media Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Apple UI Inspired Styling (via Markdown/HTML) ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1C1C1E; /* Darker text */
        background-color: #F2F2F7; /* Light background inspired by Apple */
    }
    .stApp {
        max-width: 1200px;
        margin: auto;
        padding: 2rem;
        background-color: #FFFFFF; /* White main content area */
        border-radius: 16px; /* Rounded corners for the main app */
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); /* Softer shadow */
        border: 1px solid #E5E5EA; /* Subtle border */
    }
    h1, h2, h3, h4, h5, h6 {
        color: #1C1C1E; /* Darker titles */
        font-weight: 600; /* Semibold */
    }
    .stFileUploader > div > button {
        background-color: #007AFF; /* Apple Blue */
        color: white;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 2px 5px rgba(0, 122, 255, 0.2);
        transition: all 0.2s ease-in-out;
    }
    .stFileUploader > div > button:hover {
        background-color: #0056B3; /* Darker blue on hover */
        box-shadow: 0 4px 10px rgba(0, 122, 255, 0.3);
    }
    .stFileUploader > div > p {
        color: #6B7280; /* Gray text for file uploader info */
    }
    .stAlert {
        border-radius: 8px;
        font-weight: 500;
    }
    .stAlert > div {
        border-radius: 8px;
    }
    .stAlert.success {
        background-color: #E6F7ED; /* Light green */
        color: #22C55E; /* System Green */
        border-left: 5px solid #22C55E;
    }
    .stAlert.error {
        background-color: #FEE8E8; /* Light red */
        color: #EF4444; /* System Red */
        border-left: 5px solid #EF4444;
    }
    .stMarkdown {
        color: #4A4A4A; /* Slightly lighter text for general content */
    }
    .stCode {
        background-color: #F0F0F5; /* Light gray for code blocks */
        border-radius: 6px;
        padding: 0.2em 0.4em;
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
        color: #333333;
    }
    .chart-container {
        background-color: #FFFFFF;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05); /* Lighter shadow for chart cards */
        padding: 1.5rem;
        margin-bottom: 2rem;
        border: 1px solid #F0F0F5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Apple Color Palette ---
apple_colors = {
    'blue': '#007AFF',
    'green': '#34C759',
    'red': '#FF3B30',
    'orange': '#FF9500',
    'purple': '#AF52DE',
    'gray': '#8E8E93',
    'lightGray': '#E5E5EA',
    'darkGray': '#1C1C1E'
}

# --- Title ---
st.markdown("<h1 style='text-align: center;'>Interactive Media Intelligence Dashboard</h1>", unsafe_allow_html=True)

# --- How to Use Section ---
st.markdown(
    """
    <div class="chart-container">
        <h2 title="Provides an overview and instructions for using the dashboard.">How to Use This Dashboard</h2>
        <p>Welcome to your Interactive Media Intelligence Dashboard! Follow the steps below to upload your data and visualize key insights. Hover over section titles and input fields for more information.</p>
        <ul>
            <li><strong>Step 1:</strong> Upload your CSV file containing media data.</li>
            <li><strong>Step 2:</strong> The dashboard will automatically clean and prepare your data.</li>
            <li><strong>Step 3:</strong> Explore interactive charts and insights generated from your data.</li>
            <li><strong>Step 4:</strong> (New!) Enter your OpenRouter API key and select a model to generate AI-powered campaign recommendations and chart insights.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Section 1: CSV Upload ---
st.markdown(
    """
    <div class="chart-container">
        <h2 title="Uploads your CSV file for analysis.">1. Upload Your CSV File</h2>
        <p>Please upload a CSV file with the following columns: <code class="stCode">Date</code>, <code class="stCode">Platform</code>, <code class="stCode">Sentiment</code>, <code class="stCode">Location</code>, <code class="stCode">Engagements</code>, <code class="stCode">Media Type</code>.</p>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Select CSV File",
    type="csv",
    help="Click to select a CSV file from your computer. Ensure it has the required columns.",
    key="csv_uploader"
)

df = None
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success(f"CSV file uploaded successfully! {len(df)} rows detected.")
    except Exception as e:
        st.error(f"Failed to read CSV file: {e}")

# --- Section 2: Data Cleaning Status ---
st.markdown(
    """
    <div class="chart-container">
        <h2 title="Displays the status of data cleaning and normalization.">2. Data Cleaning Status</h2>
        <p>This section confirms if your data has been successfully cleaned, including date conversion, filling missing engagement values, and normalizing column names.</p>
    </div>
    """,
    unsafe_allow_html=True
)

cleaned_df = None
if df is not None:
    try:
        # Normalize column names
        df.columns = df.columns.str.lower().str.replace(' ', '_')

        # Convert 'Date' to datetime, coercing errors to NaT
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Fill missing 'Engagements' with 0
        if 'engagements' in df.columns:
            df['engagements'] = pd.to_numeric(df['engagements'], errors='coerce').fillna(0).astype(int)
        else:
            st.warning("'Engagements' column not found. Some charts may not display correctly.")
            df['engagements'] = 0 # Add a placeholder column

        # Filter out rows where date conversion failed
        cleaned_df = df.dropna(subset=['date']).copy() # Use .copy() to avoid SettingWithCopyWarning

        if not cleaned_df.empty:
            st.success(f"Data cleaning complete! {len(cleaned_df)} valid rows processed.")
        else:
            st.warning("No valid data found after cleaning. Please check your CSV file format and 'Date' column.")
            cleaned_df = None

    except Exception as e:
        st.error(f"Error during data cleaning: {e}")
        cleaned_df = None
else:
    st.info("Awaiting CSV file upload for data cleaning.")

# --- AI Capabilities Section ---
st.markdown(
    """
    <div class="chart-container">
        <h2 title="Configure AI models for campaign recommendations and insights generation.">4. AI Capabilities (Powered by OpenRouter)</h2>
        <p>Enter your OpenRouter API key and select a model to enable AI-powered campaign recommendations and dynamic chart insights.</p>
    </div>
    """,
    unsafe_allow_html=True
)

openrouter_api_key = st.text_input(
    "OpenRouter API Key",
    type="password",
    help="Enter your API key from OpenRouter.ai (e.g., sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx)",
    key="openrouter_api_key"
)

# Recommended free models on OpenRouter
recommended_models = {
    "Mistral 7B Instruct": "mistralai/mistral-7b-instruct",
    "Google Gemini-2.0-flash": "google/gemini-2.0-flash-exp:free",
    "Deepseek-r1": "deepseek/deepseek-r1-distill-llama-70b:free",
}

selected_model_display = st.selectbox(
    "Select AI Model",
    options=list(recommended_models.keys()),
    help="Choose a free model from OpenRouter for generating insights and recommendations.",
    key="ai_model_selector"
)
selected_model_id = recommended_models[selected_model_display]

# Initialize OpenAI client
client = None
if openrouter_api_key:
    try:
        client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_api_key,
        )
    except Exception as e:
        st.error(f"Error initializing OpenAI client: {e}")
        client = None

# Function to generate text using OpenAI/OpenRouter
def generate_text_with_ai(prompt, model, client_obj):
    if not client_obj:
        st.error("AI client not initialized. Please provide a valid API key.")
        return "AI client not available."
    try:
        response = client_obj.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500,
        )
        return response.choices[0].message.content
    except openai.APIConnectionError as e:
        st.error(f"Could not connect to OpenRouter API: {e}. Please check your internet connection or API key.")
        return "Error: Could not connect to API."
    except openai.APIStatusError as e:
        st.error(f"OpenRouter API returned an error: {e.status_code} - {e.response}. Please check your API key or model availability.")
        return "Error: API call failed."
    except Exception as e:
        st.error(f"An unexpected error occurred during AI generation: {e}")
        return "Error: Unexpected AI generation error."

# --- Overall Campaign Recommendation ---
if cleaned_df is not None and not cleaned_df.empty and client:
    st.markdown(
        """
        <div class="chart-container">
            <h2 title="Generates an overall campaign recommendation based on your media data.">Overall Campaign Recommendation</h2>
            <p>This AI-powered recommendation provides insights into what's working and what needs improvement in your media campaigns.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Generate Campaign Recommendation", key="generate_campaign_btn"):
        with st.spinner("Generating campaign recommendation..."):
            # Summarize data for the LLM
            data_summary = f"""
            Overall Data Summary:
            Total entries: {len(cleaned_df)}
            Date range: {cleaned_df['date'].min().strftime('%Y-%m-%d')} to {cleaned_df['date'].max().strftime('%Y-%m-%d')}

            Sentiment Breakdown:
            {cleaned_df['sentiment'].value_counts().to_dict()}

            Top 5 Platforms by Engagements:
            {cleaned_df.groupby('platform')['engagements'].sum().nlargest(5).to_dict()}

            Top 5 Media Types by Count:
            {cleaned_df['media_type'].value_counts().nlargest(5).to_dict()}

            Top 5 Locations by Engagements:
            {cleaned_df.groupby('location')['engagements'].sum().nlargest(5).to_dict()}

            Engagement trend (first 5 and last 5 dates):
            {cleaned_df.groupby(cleaned_df['date'].dt.date)['engagements'].sum().head(5).to_dict()}
            ...
            {cleaned_df.groupby(cleaned_df['date'].dt.date)['engagements'].sum().tail(5).to_dict()}
            """

            campaign_prompt = f"""
            Analyze the following media intelligence data. Based on the sentiment breakdown, engagement trends, platform performance, media type mix, and top locations, provide a concise campaign recommendation.
            The recommendation should clearly state 'What's Working' and 'What Needs to be Improved' to optimize future media strategies. Focus on actionable advice.

            {data_summary}

            Campaign Recommendation:
            """
            recommendation = generate_text_with_ai(campaign_prompt, selected_model_id, client)
            st.markdown(f"<div class='chart-container'><p>{recommendation}</p></div>", unsafe_allow_html=True)
else:
    if cleaned_df is None or cleaned_df.empty:
        st.info("Upload a CSV and ensure data cleaning is complete to enable AI capabilities.")
    elif not openrouter_api_key:
        st.info("Please enter your OpenRouter API Key to enable AI capabilities.")


# --- Section 3: Interactive Charts ---
if cleaned_df is not None and not cleaned_df.empty:
    st.markdown(
        """
        <div class="chart-container">
            <h2 title="Visualizes your media data through interactive charts and provides key insights.">3. Interactive Charts & Insights</h2>
            <p>Explore the various aspects of your media data through these interactive visualizations. Each chart now comes with AI-generated insights to help you understand your media performance.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Function to generate chart insights
    def get_chart_insights(chart_title, data_description, client_obj, model_id):
        prompt = f"""
        Given the following data for a "{chart_title}" chart:
        {data_description}

        Provide 3 concise and actionable insights based on this data. Format them as a bulleted list.
        """
        return generate_text_with_ai(prompt, model_id, client_obj)

    # --- Sentiment Breakdown Pie Chart ---
    st.markdown(
        """
        <div class="chart-container">
            <h3 title="A pie chart showing the distribution of positive, negative, and neutral sentiments in your data.">Sentiment Breakdown</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    if 'sentiment' in cleaned_df.columns:
        sentiment_counts = cleaned_df['sentiment'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']
        fig_sentiment = px.pie(
            sentiment_counts,
            values='Count',
            names='Sentiment',
            hole=0.4,
            color_discrete_sequence=[apple_colors['red'], apple_colors['orange'], apple_colors['green'], apple_colors['gray']],
            title='Sentiment Breakdown'
        )
        fig_sentiment.update_layout(
            font_family="Inter",
            title_font_color=apple_colors['darkGray'],
            title_x=0.5,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(bgcolor='rgba(255,255,255,0.7)', bordercolor=apple_colors['lightGray'], borderwidth=1, font=dict(color=apple_colors['darkGray']))
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)

        if client:
            if st.button(f"Generate Insights for Sentiment Breakdown", key="insights_sentiment"):
                with st.spinner("Generating insights..."):
                    insights = get_chart_insights(
                        "Sentiment Breakdown",
                        f"Sentiment distribution: {sentiment_counts.set_index('Sentiment').to_dict()['Count']}",
                        client, selected_model_id
                    )
                    st.markdown(f"<h4 style='color: #4A4A4A; font-weight: 500; margin-top: 1.5rem; margin-bottom: 0.5rem;'>Top 3 Insights:</h4>", unsafe_allow_html=True)
                    st.markdown(f"<ul style='color: #6B7280; list-style-type: disc; margin-left: 20px; padding-left: 0;'>{insights}</ul>", unsafe_allow_html=True)
        else:
            st.info("Enter API key and select model to generate AI insights for this chart.")
    else:
        st.warning("Sentiment column not found in the uploaded CSV. Cannot generate Sentiment Breakdown chart.")

    # --- Engagement Trend over Time Line Chart ---
    st.markdown(
        """
        <div class="chart-container">
            <h3 title="A line chart illustrating how total engagements evolve over time.">Engagement Trend Over Time</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    if 'date' in cleaned_df.columns and 'engagements' in cleaned_df.columns:
        engagement_by_date = cleaned_df.groupby(cleaned_df['date'].dt.date)['engagements'].sum().reset_index()
        engagement_by_date.columns = ['Date', 'Total Engagements']
        fig_engagement_trend = px.line(
            engagement_by_date,
            x='Date',
            y='Total Engagements',
            title='Engagement Trend Over Time',
            color_discrete_sequence=[apple_colors['blue']]
        )
        fig_engagement_trend.update_traces(mode='lines+markers', marker=dict(symbol='circle-open', size=6, line=dict(width=1, color=apple_colors['blue'])))
        fig_engagement_trend.update_layout(
            font_family="Inter",
            title_font_color=apple_colors['darkGray'],
            title_x=0.5,
            xaxis_title_font_color=apple_colors['gray'],
            yaxis_title_font_color=apple_colors['gray'],
            xaxis_tickfont_color=apple_colors['gray'],
            yaxis_tickfont_color=apple_colors['gray'],
            xaxis_gridcolor=apple_colors['lightGray'],
            yaxis_gridcolor=apple_colors['lightGray'],
            xaxis_linecolor=apple_colors['lightGray'],
            yaxis_linecolor=apple_colors['lightGray'],
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig_engagement_trend, use_container_width=True)

        if client:
            if st.button(f"Generate Insights for Engagement Trend", key="insights_engagement_trend"):
                with st.spinner("Generating insights..."):
                    # Provide a sample of the data to avoid sending too much
                    data_sample = engagement_by_date.head(5).to_string(index=False) + "\n..." + engagement_by_date.tail(5).to_string(index=False)
                    insights = get_chart_insights(
                        "Engagement Trend Over Time",
                        f"Engagement data over time (sample):\n{data_sample}",
                        client, selected_model_id
                    )
                    st.markdown(f"<h4 style='color: #4A4A4A; font-weight: 500; margin-top: 1.5rem; margin-bottom: 0.5rem;'>Top 3 Insights:</h4>", unsafe_allow_html=True)
                    st.markdown(f"<ul style='color: #6B7280; list-style-type: disc; margin-left: 20px; padding-left: 0;'>{insights}</ul>", unsafe_allow_html=True)
        else:
            st.info("Enter API key and select model to generate AI insights for this chart.")
    else:
        st.warning("Date or Engagements column not found in the uploaded CSV. Cannot generate Engagement Trend chart.")

    # --- Platform Engagements Bar Chart ---
    st.markdown(
        """
        <div class="chart-container">
            <h3 title="A bar chart displaying the total engagements across different platforms.">Platform Engagements</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    if 'platform' in cleaned_df.columns and 'engagements' in cleaned_df.columns:
        platform_engagements = cleaned_df.groupby('platform')['engagements'].sum().reset_index()
        platform_engagements.columns = ['Platform', 'Total Engagements']
        fig_platform = px.bar(
            platform_engagements,
            x='Platform',
            y='Total Engagements',
            title='Platform Engagements',
            color_discrete_sequence=[apple_colors['purple']]
        )
        fig_platform.update_layout(
            font_family="Inter",
            title_font_color=apple_colors['darkGray'],
            title_x=0.5,
            xaxis_title_font_color=apple_colors['gray'],
            yaxis_title_font_color=apple_colors['gray'],
            xaxis_tickfont_color=apple_colors['gray'],
            yaxis_tickfont_color=apple_colors['gray'],
            xaxis_gridcolor=apple_colors['lightGray'],
            yaxis_gridcolor=apple_colors['lightGray'],
            xaxis_linecolor=apple_colors['lightGray'],
            yaxis_linecolor=apple_colors['lightGray'],
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig_platform, use_container_width=True)

        if client:
            if st.button(f"Generate Insights for Platform Engagements", key="insights_platform"):
                with st.spinner("Generating insights..."):
                    insights = get_chart_insights(
                        "Platform Engagements",
                        f"Platform engagements: {platform_engagements.set_index('Platform').to_dict()['Total Engagements']}",
                        client, selected_model_id
                    )
                    st.markdown(f"<h4 style='color: #4A4A4A; font-weight: 500; margin-top: 1.5rem; margin-bottom: 0.5rem;'>Top 3 Insights:</h4>", unsafe_allow_html=True)
                    st.markdown(f"<ul style='color: #6B7280; list-style-type: disc; margin-left: 20px; padding-left: 0;'>{insights}</ul>", unsafe_allow_html=True)
        else:
            st.info("Enter API key and select model to generate AI insights for this chart.")
    else:
        st.warning("Platform or Engagements column not found in the uploaded CSV. Cannot generate Platform Engagements chart.")

    # --- Media Type Mix Pie Chart ---
    st.markdown(
        """
        <div class="chart-container">
            <h3 title="A pie chart showing the proportion of different media types in your dataset.">Media Type Mix</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    if 'media_type' in cleaned_df.columns:
        media_type_counts = cleaned_df['media_type'].value_counts().reset_index()
        media_type_counts.columns = ['Media Type', 'Count']
        fig_media_type = px.pie(
            media_type_counts,
            values='Count',
            names='Media Type',
            hole=0.4,
            color_discrete_sequence=[apple_colors['orange'], apple_colors['green'], apple_colors['blue'], apple_colors['gray']],
            title='Media Type Mix'
        )
        fig_media_type.update_layout(
            font_family="Inter",
            title_font_color=apple_colors['darkGray'],
            title_x=0.5,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(bgcolor='rgba(255,255,255,0.7)', bordercolor=apple_colors['lightGray'], borderwidth=1, font=dict(color=apple_colors['darkGray']))
        )
        st.plotly_chart(fig_media_type, use_container_width=True)

        if client:
            if st.button(f"Generate Insights for Media Type Mix", key="insights_media_type"):
                with st.spinner("Generating insights..."):
                    insights = get_chart_insights(
                        "Media Type Mix",
                        f"Media type distribution: {media_type_counts.set_index('Media Type').to_dict()['Count']}",
                        client, selected_model_id
                    )
                    st.markdown(f"<h4 style='color: #4A4A4A; font-weight: 500; margin-top: 1.5rem; margin-bottom: 0.5rem;'>Top 3 Insights:</h4>", unsafe_allow_html=True)
                    st.markdown(f"<ul style='color: #6B7280; list-style-type: disc; margin-left: 20px; padding-left: 0;'>{insights}</ul>", unsafe_allow_html=True)
        else:
            st.info("Enter API key and select model to generate AI insights for this chart.")
    else:
        st.warning("Media Type column not found in the uploaded CSV. Cannot generate Media Type Mix chart.")

    # --- Top 5 Locations Bar Chart ---
    st.markdown(
        """
        <div class="chart-container">
            <h3 title="A bar chart highlighting the top 5 geographical locations by total engagements.">Top 5 Locations by Engagement</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    if 'location' in cleaned_df.columns and 'engagements' in cleaned_df.columns:
        location_engagements = cleaned_df.groupby('location')['engagements'].sum().nlargest(5).reset_index()
        location_engagements.columns = ['Location', 'Total Engagements']
        fig_locations = px.bar(
            location_engagements,
            x='Location',
            y='Total Engagements',
            title='Top 5 Locations by Engagement',
            color_discrete_sequence=[apple_colors['blue']]
        )
        fig_locations.update_layout(
            font_family="Inter",
            title_font_color=apple_colors['darkGray'],
            title_x=0.5,
            xaxis_title_font_color=apple_colors['gray'],
            yaxis_title_font_color=apple_colors['gray'],
            xaxis_tickfont_color=apple_colors['gray'],
            yaxis_tickfont_color=apple_colors['gray'],
            xaxis_gridcolor=apple_colors['lightGray'],
            yaxis_gridcolor=apple_colors['lightGray'],
            xaxis_linecolor=apple_colors['lightGray'],
            yaxis_linecolor=apple_colors['lightGray'],
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig_locations, use_container_width=True)

        if client:
            if st.button(f"Generate Insights for Top 5 Locations", key="insights_locations"):
                with st.spinner("Generating insights..."):
                    insights = get_chart_insights(
                        "Top 5 Locations by Engagement",
                        f"Top 5 locations by engagement: {location_engagements.set_index('Location').to_dict()['Total Engagements']}",
                        client, selected_model_id
                    )
                    st.markdown(f"<h4 style='color: #4A4A4A; font-weight: 500; margin-top: 1.5rem; margin-bottom: 0.5rem;'>Top 3 Insights:</h4>", unsafe_allow_html=True)
                    st.markdown(f"<ul style='color: #6B7280; list-style-type: disc; margin-left: 20px; padding-left: 0;'>{insights}</ul>", unsafe_allow_html=True)
        else:
            st.info("Enter API key and select model to generate AI insights for this chart.")
    else:
        st.warning("Location or Engagements column not found in the uploaded CSV. Cannot generate Top 5 Locations chart.")

elif uploaded_file is not None and (cleaned_df is None or cleaned_df.empty):
    st.error("Could not process data. Please ensure your CSV file has the required columns and valid data.")

