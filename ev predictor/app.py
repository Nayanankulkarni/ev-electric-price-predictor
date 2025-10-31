import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Electric Vehicle Data Explorer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with modern design
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Main background with gradient */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Content container */
    .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 1rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    /* Metrics styling */
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
        color: white;
    }
    
    .stMetric label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    
    /* Headers */
    h1 {
        color: #1e293b;
        font-weight: 800;
        font-size: 3rem !important;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2, h3 {
        color: #334155;
        font-weight: 700;
    }
    
    /* Sidebar styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
    }
    
    .css-1d391kg .stSelectbox label,
    .css-1d391kg .stSlider label,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f1f5f9;
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        background-color: transparent;
        color: #64748b;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Subtitle styling */
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    /* Card styling */
    .info-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    
    /* Download button */
    .stDownloadButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stDownloadButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.5);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-top: 30px;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('ElectricCarData_Clean (1).csv')
    df.columns = df.columns.str.strip()
    df['Brand'] = df['Brand'].str.strip()
    df['Model'] = df['Model'].str.strip()
    df['FastCharge_KmH'] = pd.to_numeric(df['FastCharge_KmH'], errors='coerce')
    return df

df = load_data()

# Animated Header
st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1>⚡ Electric Vehicle Data Explorer</h1>
        <p class='subtitle'>Discover, Compare & Analyze the Future of Mobility</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar with enhanced styling
st.sidebar.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h2 style='color: white; font-size: 1.5rem;'>🔍 Filter Options</h2>
    </div>
    """, unsafe_allow_html=True)

# Brand filter
brands = ['All'] + sorted(df['Brand'].unique().tolist())
selected_brand = st.sidebar.selectbox("🏭 Select Brand", brands)

# Price range filter
price_range = st.sidebar.slider(
    "💰 Price Range (€)",
    min_value=int(df['PriceEuro'].min()),
    max_value=int(df['PriceEuro'].max()),
    value=(int(df['PriceEuro'].min()), int(df['PriceEuro'].max())),
    format="€%d"
)

# Range filter
range_filter = st.sidebar.slider(
    "🔋 Range (km)",
    min_value=int(df['Range_Km'].min()),
    max_value=int(df['Range_Km'].max()),
    value=(int(df['Range_Km'].min()), int(df['Range_Km'].max()))
)

# Body style filter
body_styles = ['All'] + sorted(df['BodyStyle'].unique().tolist())
selected_body = st.sidebar.selectbox("🚗 Body Style", body_styles)

# PowerTrain filter
powertrains = ['All'] + sorted(df['PowerTrain'].unique().tolist())
selected_powertrain = st.sidebar.selectbox("⚙️ PowerTrain", powertrains)

# Apply filters
filtered_df = df.copy()
if selected_brand != 'All':
    filtered_df = filtered_df[filtered_df['Brand'] == selected_brand]
if selected_body != 'All':
    filtered_df = filtered_df[filtered_df['BodyStyle'] == selected_body]
if selected_powertrain != 'All':
    filtered_df = filtered_df[filtered_df['PowerTrain'] == selected_powertrain]

filtered_df = filtered_df[
    (filtered_df['PriceEuro'] >= price_range[0]) & 
    (filtered_df['PriceEuro'] <= price_range[1]) &
    (filtered_df['Range_Km'] >= range_filter[0]) & 
    (filtered_df['Range_Km'] <= range_filter[1])
]

# Key metrics with icons
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("🚗 Total Cars", f"{len(filtered_df)}")
with col2:
    st.metric("💰 Avg Price", f"€{filtered_df['PriceEuro'].mean():,.0f}")
with col3:
    st.metric("🔋 Avg Range", f"{filtered_df['Range_Km'].mean():.0f} km")
with col4:
    st.metric("🏎️ Avg Top Speed", f"{filtered_df['TopSpeed_KmH'].mean():.0f} km/h")
with col5:
    st.metric("🏭 Brands", f"{filtered_df['Brand'].nunique()}")

st.markdown("<br>", unsafe_allow_html=True)

# Main content tabs with enhanced icons
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard Overview", 
    "🏎️ Performance Metrics", 
    "🔋 Efficiency Analysis", 
    "📈 Market Insights",
    "📋 Data Explorer"
])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Price vs Range scatter with enhanced styling
        fig1 = px.scatter(
            filtered_df,
            x='Range_Km',
            y='PriceEuro',
            color='Brand',
            size='TopSpeed_KmH',
            hover_data=['Model', 'PowerTrain'],
            title='💰 Price vs Range Analysis',
            labels={'Range_Km': 'Range (km)', 'PriceEuro': 'Price (€)'},
            template='plotly_white'
        )
        fig1.update_layout(
            height=450,
            title_font_size=18,
            title_font_color='#1e293b',
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.3)
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Top 10 most expensive cars
        top_expensive = filtered_df.nlargest(10, 'PriceEuro')[['Brand', 'Model', 'PriceEuro']]
        top_expensive['Car'] = top_expensive['Brand'] + ' ' + top_expensive['Model']
        
        fig2 = px.bar(
            top_expensive,
            x='PriceEuro',
            y='Car',
            orientation='h',
            title='💎 Top 10 Most Expensive EVs',
            labels={'PriceEuro': 'Price (€)', 'Car': ''},
            color='PriceEuro',
            color_continuous_scale='Purples',
            template='plotly_white'
        )
        fig2.update_layout(
            height=450,
            title_font_size=18,
            title_font_color='#1e293b',
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Brand distribution with sunburst
        brand_counts = filtered_df['Brand'].value_counts().head(10)
        fig3 = px.pie(
            values=brand_counts.values,
            names=brand_counts.index,
            title='🏭 Top 10 Brands by Model Count',
            hole=0.5,
            template='plotly_white',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig3.update_traces(textposition='inside', textinfo='percent+label')
        fig3.update_layout(
            height=450,
            title_font_size=18,
            title_font_color='#1e293b'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        # Body style distribution
        body_counts = filtered_df['BodyStyle'].value_counts()
        fig4 = px.bar(
            x=body_counts.index,
            y=body_counts.values,
            title='🚗 Distribution by Body Style',
            labels={'x': 'Body Style', 'y': 'Count'},
            color=body_counts.values,
            color_continuous_scale='Viridis',
            template='plotly_white'
        )
        fig4.update_layout(
            height=450,
            title_font_size=18,
            title_font_color='#1e293b',
            showlegend=False
        )
        st.plotly_chart(fig4, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Acceleration vs Top Speed
        fig5 = px.scatter(
            filtered_df,
            x='AccelSec',
            y='TopSpeed_KmH',
            color='PowerTrain',
            size='PriceEuro',
            hover_data=['Brand', 'Model'],
            title='🚀 Acceleration vs Top Speed',
            labels={'AccelSec': '0-100 km/h (seconds)', 'TopSpeed_KmH': 'Top Speed (km/h)'},
            template='plotly_white'
        )
        fig5.update_layout(
            height=450,
            title_font_size=18,
            title_font_color='#1e293b'
        )
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        # Fastest cars
        fastest = filtered_df.nlargest(10, 'TopSpeed_KmH')[['Brand', 'Model', 'TopSpeed_KmH', 'AccelSec']]
        fastest['Car'] = fastest['Brand'] + ' ' + fastest['Model']
        
        fig6 = px.bar(
            fastest,
            x='TopSpeed_KmH',
            y='Car',
            orientation='h',
            title='🏁 Top 10 Fastest EVs',
            labels={'TopSpeed_KmH': 'Top Speed (km/h)', 'Car': ''},
            color='TopSpeed_KmH',
            color_continuous_scale='Reds',
            template='plotly_white'
        )
        fig6.update_layout(
            height=450,
            title_font_size=18,
            title_font_color='#1e293b',
            showlegend=False
        )
        st.plotly_chart(fig6, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # PowerTrain comparison - Multi-metric
        powertrain_stats = filtered_df.groupby('PowerTrain').agg({
            'AccelSec': 'mean',
            'TopSpeed_KmH': 'mean',
            'Range_Km': 'mean'
        }).reset_index()
        
        fig7 = go.Figure()
        fig7.add_trace(go.Bar(
            name='Avg Acceleration (s)',
            x=powertrain_stats['PowerTrain'],
            y=powertrain_stats['AccelSec'],
            marker_color='#667eea'
        ))
        fig7.update_layout(
            title='⚙️ Average Acceleration by PowerTrain',
            height=450,
            title_font_size=18,
            title_font_color='#1e293b',
            template='plotly_white'
        )
        st.plotly_chart(fig7, use_container_width=True)
    
    with col4:
        # Fast charge speed
        fc_df = filtered_df.dropna(subset=['FastCharge_KmH'])
        if len(fc_df) > 0:
            fig8 = px.box(
                fc_df,
                x='PowerTrain',
                y='FastCharge_KmH',
                title='⚡ Fast Charging Speed by PowerTrain',
                labels={'FastCharge_KmH': 'Fast Charge (km/h)', 'PowerTrain': 'PowerTrain'},
                color='PowerTrain',
                template='plotly_white',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig8.update_layout(
                height=450,
                title_font_size=18,
                title_font_color='#1e293b'
            )
            st.plotly_chart(fig8, use_container_width=True)
        else:
            st.info("⚠️ No fast charging data available for selected filters")

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        # Efficiency vs Range
        fig9 = px.scatter(
            filtered_df,
            x='Efficiency_WhKm',
            y='Range_Km',
            color='BodyStyle',
            size='PriceEuro',
            hover_data=['Brand', 'Model'],
            title='🔋 Efficiency vs Range Analysis',
            labels={'Efficiency_WhKm': 'Efficiency (Wh/km)', 'Range_Km': 'Range (km)'},
            template='plotly_white'
        )
        fig9.update_layout(
            height=450,
            title_font_size=18,
            title_font_color='#1e293b'
        )
        st.plotly_chart(fig9, use_container_width=True)
    
    with col2:
        # Best range cars
        best_range = filtered_df.nlargest(10, 'Range_Km')[['Brand', 'Model', 'Range_Km', 'Efficiency_WhKm']]
        best_range['Car'] = best_range['Brand'] + ' ' + best_range['Model']
        
        fig10 = px.bar(
            best_range,
            x='Range_Km',
            y='Car',
            orientation='h',
            title='🏆 Top 10 Longest Range EVs',
            labels={'Range_Km': 'Range (km)', 'Car': ''},
            color='Range_Km',
            color_continuous_scale='Greens',
            template='plotly_white'
        )
        fig10.update_layout(
            height=450,
            title_font_size=18,
            title_font_color='#1e293b',
            showlegend=False
        )
        st.plotly_chart(fig10, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Most efficient cars
        most_efficient = filtered_df.nsmallest(10, 'Efficiency_WhKm')[['Brand', 'Model', 'Efficiency_WhKm']]
        most_efficient['Car'] = most_efficient['Brand'] + ' ' + most_efficient['Model']
        
        fig11 = px.bar(
            most_efficient,
            x='Efficiency_WhKm',
            y='Car',
            orientation='h',
            title='💡 Top 10 Most Efficient EVs',
            labels={'Efficiency_WhKm': 'Efficiency (Wh/km)', 'Car': ''},
            color='Efficiency_WhKm',
            color_continuous_scale='Teal',
            template='plotly_white'
        )
        fig11.update_layout(
            height=450,
            title_font_size=18,
            title_font_color='#1e293b',
            showlegend=False
        )
        st.plotly_chart(fig11, use_container_width=True)
    
    with col4:
        # Rapid charge availability
        rapid_charge = filtered_df['RapidCharge'].value_counts()
        fig12 = px.pie(
            values=rapid_charge.values,
            names=rapid_charge.index,
            title='⚡ Rapid Charge Availability',
            hole=0.5,
            template='plotly_white',
            color_discrete_sequence=['#10b981', '#ef4444']
        )
        fig12.update_traces(textposition='inside', textinfo='percent+label')
        fig12.update_layout(
            height=450,
            title_font_size=18,
            title_font_color='#1e293b'
        )
        st.plotly_chart(fig12, use_container_width=True)

with tab4:
    st.markdown("### 📈 Market Insights & Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Price distribution histogram
        fig13 = px.histogram(
            filtered_df,
            x='PriceEuro',
            nbins=30,
            title='💰 Price Distribution',
            labels={'PriceEuro': 'Price (€)', 'count': 'Number of Models'},
            template='plotly_white',
            color_discrete_sequence=['#667eea']
        )
        fig13.update_layout(
            height=400,
            title_font_size=18,
            title_font_color='#1e293b',
            showlegend=False
        )
        st.plotly_chart(fig13, use_container_width=True)
        
        # Range distribution
        fig14 = px.histogram(
            filtered_df,
            x='Range_Km',
            nbins=30,
            title='🔋 Range Distribution',
            labels={'Range_Km': 'Range (km)', 'count': 'Number of Models'},
            template='plotly_white',
            color_discrete_sequence=['#10b981']
        )
        fig14.update_layout(
            height=400,
            title_font_size=18,
            title_font_color='#1e293b',
            showlegend=False
        )
        st.plotly_chart(fig14, use_container_width=True)
    
    with col2:
        # Average specs by brand (top 10)
        top_brands = filtered_df['Brand'].value_counts().head(10).index
        brand_avg = filtered_df[filtered_df['Brand'].isin(top_brands)].groupby('Brand').agg({
            'PriceEuro': 'mean',
            'Range_Km': 'mean',
            'TopSpeed_KmH': 'mean'
        }).reset_index()
        
        fig15 = go.Figure()
        fig15.add_trace(go.Bar(
            name='Avg Price (€)',
            x=brand_avg['Brand'],
            y=brand_avg['PriceEuro'],
            marker_color='#667eea'
        ))
        fig15.update_layout(
            title='📊 Average Price by Top 10 Brands',
            height=400,
            title_font_size=18,
            title_font_color='#1e293b',
            template='plotly_white',
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig15, use_container_width=True)
        
        # Correlation heatmap
        corr_data = filtered_df[['PriceEuro', 'Range_Km', 'TopSpeed_KmH', 'AccelSec', 'Efficiency_WhKm']].corr()
        fig16 = px.imshow(
            corr_data,
            title='🔗 Correlation Matrix',
            labels=dict(color="Correlation"),
            color_continuous_scale='RdBu',
            template='plotly_white',
            aspect="auto"
        )
        fig16.update_layout(
            height=400,
            title_font_size=18,
            title_font_color='#1e293b'
        )
        st.plotly_chart(fig16, use_container_width=True)

with tab5:
    st.markdown("### 📋 Detailed Vehicle Data Explorer")
    
    # Search functionality
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍 Search by Brand or Model", "", placeholder="Type to search...")
    with col2:
        sort_by = st.selectbox("Sort by", ['Price', 'Range', 'Top Speed', 'Efficiency'])
    
    if search:
        filtered_df = filtered_df[
            filtered_df['Brand'].str.contains(search, case=False, na=False) |
            filtered_df['Model'].str.contains(search, case=False, na=False)
        ]
    
    # Sort data
    sort_map = {
        'Price': 'PriceEuro',
        'Range': 'Range_Km',
        'Top Speed': 'TopSpeed_KmH',
        'Efficiency': 'Efficiency_WhKm'
    }
    filtered_df = filtered_df.sort_values(sort_map[sort_by], ascending=False)
    
    # Display info cards for top 3
    st.markdown("#### 🏆 Top 3 Vehicles (by selected sort)")
    cols = st.columns(3)
    for idx, (i, row) in enumerate(filtered_df.head(3).iterrows()):
        with cols[idx]:
            st.markdown(f"""
                <div class='info-card'>
                    <h4 style='color: #667eea; margin: 0;'>{row['Brand']} {row['Model']}</h4>
                    <p style='margin: 5px 0;'><strong>💰 Price:</strong> €{row['PriceEuro']:,.0f}</p>
                    <p style='margin: 5px 0;'><strong>🔋 Range:</strong> {row['Range_Km']:.0f} km</p>
                    <p style='margin: 5px 0;'><strong>🏎️ Top Speed:</strong> {row['TopSpeed_KmH']:.0f} km/h</p>
                    <p style='margin: 5px 0;'><strong>⚡ 0-100:</strong> {row['AccelSec']:.1f}s</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Prepare display dataframe
    display_df = filtered_df.copy()
    display_df['PriceEuro'] = display_df['PriceEuro'].apply(lambda x: f"€{x:,.0f}")
    display_df['AccelSec'] = display_df['AccelSec'].apply(lambda x: f"{x:.1f}s")
    display_df['TopSpeed_KmH'] = display_df['TopSpeed_KmH'].apply(lambda x: f"{x:.0f} km/h")
    display_df['Range_Km'] = display_df['Range_Km'].apply(lambda x: f"{x:.0f} km")
    display_df['Efficiency_WhKm'] = display_df['Efficiency_WhKm'].apply(lambda x: f"{x:.0f} Wh/km")
    display_df['FastCharge_KmH'] = display_df['FastCharge_KmH'].apply(
        lambda x: f"{x:.0f} km/h" if pd.notna(x) else "N/A"
    )
    
    # Display dataframe
    st.dataframe(
        display_df,
        use_container_width=True,
        height=500
    )
    
    # Download button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name="filtered_ev_data.csv",
            mime="text/csv",
            use_container_width=True
        )

# Footer
st.markdown("""
    <div class='footer'>
        <h3 style='color: white; margin-bottom: 10px;'>⚡ Electric Vehicle Data Explorer</h3>
        <p style='margin: 5px 0;'>Built with ❤️ using Streamlit & Plotly</p>
        <p style='margin: 5px 0; font-size: 0.9rem;'>Empowering sustainable transportation decisions</p>
    </div>
    """, unsafe_allow_html=True)