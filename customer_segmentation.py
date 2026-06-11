import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans

# PAGE CONFIG

st.set_page_config(
    page_title="CustomerIQ",
    page_icon="🚀",
    layout="wide"
)

# CSS

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]{
    font-family:'Poppins',sans-serif;
}

.stApp{
    background: linear-gradient(
        135deg,
        #020617,
        #0f172a,
        #1e1b4b,
        #111827
    );
    color:white;
}

h1,h2,h3,h4{
    color:white !important;
}

[data-testid="stSidebar"]{
    background:rgba(255,255,255,0.05);
    backdrop-filter:blur(20px);
}

div[data-testid="metric-container"]{
    background:rgba(255,255,255,0.08);
    border-radius:18px;
    padding:15px;
    border:1px solid rgba(255,255,255,0.1);
}

.block-container{
    padding-top:2rem;
}

</style>
""", unsafe_allow_html=True)

# HEADER

st.markdown("""
<h1 style='text-align:center'>
🚀 CustomerIQ
</h1>

<h4 style='text-align:center;color:#cbd5e1'>
AI Powered Customer Intelligence Platform
</h4>
""", unsafe_allow_html=True)

st.markdown("---")

# SIDEBAR

st.sidebar.markdown("""
# 🚀 CustomerIQ
### AI Customer Intelligence
""")

page = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "Segmentation",
        "Insights"
    ]
)

# FILE UPLOADER

uploaded_file = st.file_uploader(
    "Upload Mall_Customers.csv",
    type=["csv"]
)

if uploaded_file:

    try:

        df = pd.read_csv(uploaded_file)

        required_cols = [
            "Age",
            "Annual Income (k$)",
            "Spending Score (1-100)"
        ]

        missing = [
            col for col in required_cols
            if col not in df.columns
        ]

        if missing:
            st.error(
                f"Missing columns: {missing}"
            )
            st.stop()

        # KMEANS CLUSTERING

        X = df[
            [
                "Annual Income (k$)",
                "Spending Score (1-100)"
            ]
        ]

        kmeans = KMeans(
            n_clusters=5,
            random_state=42,
            n_init=10
        )

        df["Cluster"] = kmeans.fit_predict(X)

        cluster_colors = {
            "0": "#06b6d4",
            "1": "#10b981",
            "2": "#facc15",
            "3": "#3b82f6",
            "4": "#8b5cf6"
        }

        # DASHBOARD PAGE

        if page == "Dashboard":

            st.subheader("📊 Business Overview")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "Customers",
                len(df)
            )

            c2.metric(
                "Average Age",
                round(df["Age"].mean(), 1)
            )

            c3.metric(
                "Average Income",
                round(
                    df["Annual Income (k$)"].mean(),
                    1
                )
            )

            c4.metric(
                "Average Spending",
                round(
                    df["Spending Score (1-100)"].mean(),
                    1
                )
            )

            st.markdown("---")

            # DISTRIBUTION CHARTS

            col1, col2 = st.columns(2)

            with col1:

                fig_age = px.histogram(
                    df,
                    x="Age",
                    nbins=20,
                    title="Age Distribution",
                    template="plotly_dark"
                )

                fig_age.update_layout(
                    paper_bgcolor="#0f172a",
                    plot_bgcolor="#0f172a",
                    font_color="white"
                )

                st.plotly_chart(
                    fig_age,
                    use_container_width=True
                )

            with col2:

                fig_income = px.histogram(
                    df,
                    x="Annual Income (k$)",
                    nbins=20,
                    title="Income Distribution",
                    template="plotly_dark"
                )

                fig_income.update_layout(
                    paper_bgcolor="#0f172a",
                    plot_bgcolor="#0f172a",
                    font_color="white"
                )

                st.plotly_chart(
                    fig_income,
                    use_container_width=True
                )

            st.markdown("---")

            # CENTERED DONUT CHART

            st.subheader(
                "🎯 Customer Distribution by Cluster"
            )

            left, center, right = st.columns([1,3,1])

            with center:

                fig_pie = px.pie(
                    df,
                    names="Cluster",
                    hole=0.65,
                    title="Customer Segments Distribution",
                    color=df["Cluster"].astype(str),
                    color_discrete_map=cluster_colors,
                    template="plotly_dark"
                )

                fig_pie.update_traces(
                    textinfo="percent+label",
                    textfont_size=14
                )

                fig_pie.update_layout(
                    showlegend=False,
                    height=650,
                    paper_bgcolor="#0f172a",
                    plot_bgcolor="#0f172a",
                    font_color="white",
                    margin=dict(
                        l=0,
                        r=0,
                        t=60,
                        b=0
                    )
                )

                st.plotly_chart(
                    fig_pie,
                    use_container_width=True
                )

        # SEGMENTATION PAGE
        
        elif page == "Segmentation":

            st.subheader(
                "🎯 Customer Segmentation Analysis"
            )

            fig = px.scatter(
                df,
                x="Annual Income (k$)",
                y="Spending Score (1-100)",
                color=df["Cluster"].astype(str),
                color_discrete_map=cluster_colors,
                size="Age",
                hover_data=["Age"],
                title="Customer Clusters"
            )

            fig.update_layout(
                paper_bgcolor="#0f172a",
                plot_bgcolor="#0f172a",
                font_color="white",
                height=650
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.markdown("---")

            # CLUSTER LEGEND CARDS

            st.subheader("🌈 Cluster Categories")

            c1, c2, c3, c4, c5 = st.columns(5)

            with c1:
                st.markdown("""
                <div style="
                    background:#06b6d4;
                    padding:20px;
                    border-radius:15px;
                    text-align:center;
                    color:white;
                    font-weight:bold;
                ">
                Cluster 0
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown("""
                <div style="
                    background:#10b981;
                    padding:20px;
                    border-radius:15px;
                    text-align:center;
                    color:white;
                    font-weight:bold;
                ">
                Cluster 1
                </div>
                """, unsafe_allow_html=True)

            with c3:
                st.markdown("""
                <div style="
                    background:#facc15;
                    padding:20px;
                    border-radius:15px;
                    text-align:center;
                    color:black;
                    font-weight:bold;
                ">
                Cluster 2
                </div>
                """, unsafe_allow_html=True)

            with c4:
                st.markdown("""
                <div style="
                    background:#3b82f6;
                    padding:20px;
                    border-radius:15px;
                    text-align:center;
                    color:white;
                    font-weight:bold;
                ">
                Cluster 3
                </div>
                """, unsafe_allow_html=True)

            with c5:
                st.markdown("""
                <div style="
                    background:#8b5cf6;
                    padding:20px;
                    border-radius:15px;
                    text-align:center;
                    color:white;
                    font-weight:bold;
                ">
                Cluster 4
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            # 3D ANALYSIS
            
            st.subheader(
                "🚀 3D Cluster Analysis"
            )

            fig3d = px.scatter_3d(
                df,
                x="Annual Income (k$)",
                y="Spending Score (1-100)",
                z="Age",
                color=df["Cluster"].astype(str),
                color_discrete_map=cluster_colors,
                size="Age",
                opacity=0.8
            )

            fig3d.update_layout(
                paper_bgcolor="#0f172a",
                font_color="white",
                height=750
            )

            st.plotly_chart(
                fig3d,
                use_container_width=True
            )

        # INSIGHTS PAGE

        elif page == "Insights":

            st.subheader(
                "📈 Customer Cluster Insights"
            )

            summary = df.groupby(
                "Cluster"
            ).agg(
                {
                    "Age":"mean",
                    "Annual Income (k$)":"mean",
                    "Spending Score (1-100)":"mean"
                }
            )

            st.dataframe(
                summary,
                use_container_width=True
            )

            st.markdown("---")

            for cluster in summary.index:

                income = summary.loc[
                    cluster,
                    "Annual Income (k$)"
                ]

                spending = summary.loc[
                    cluster,
                    "Spending Score (1-100)"
                ]

                if income > 60 and spending > 60:

                    st.markdown(f"""
                    <div style="
                        background:linear-gradient(
                            135deg,
                            #10b981,
                            #065f46
                        );
                        padding:20px;
                        border-radius:15px;
                        margin-bottom:15px;
                        color:white;
                        font-size:20px;
                        font-weight:bold;
                    ">
                    👑 Cluster {cluster}: Premium Customers
                    <br>
                    High income and high spending customers.
                    Best target for premium products.
                    </div>
                    """,
                    unsafe_allow_html=True)

                elif income > 60 and spending < 50:

                    st.markdown(f"""
                    <div style="
                        background:linear-gradient(
                            135deg,
                            #3b82f6,
                            #1e3a8a
                        );
                        padding:20px;
                        border-radius:15px;
                        margin-bottom:15px;
                        color:white;
                        font-size:20px;
                        font-weight:bold;
                    ">
                    💎 Cluster {cluster}: High Income, Low Spending
                    <br>
                    Customers with strong purchasing power.
                    Needs retargeting campaigns.
                    </div>
                    """,
                    unsafe_allow_html=True)

                elif income < 50 and spending > 60:

                    st.markdown(f"""
                    <div style="
                        background:linear-gradient(
                            135deg,
                            #facc15,
                            #854d0e
                        );
                        padding:20px;
                        border-radius:15px;
                        margin-bottom:15px;
                        color:white;
                        font-size:20px;
                        font-weight:bold;
                    ">
                    ⭐ Cluster {cluster}: Potential Loyal Customers
                    <br>
                    Strong engagement.
                    Ideal for loyalty programs.
                    </div>
                    """,
                    unsafe_allow_html=True)

                else:

                    colors = [
                        ("#06b6d4", "#164e63"),
                        ("#8b5cf6", "#4c1d95"),
                        ("#ef4444", "#7f1d1d"),
                        ("#ec4899", "#831843"),
                        ("#f97316", "#7c2d12")
                    ]

                    c1, c2 = colors[
                        int(cluster) % len(colors)
                    ]

                    st.markdown(f"""
                    <div style="
                        background:linear-gradient(
                            135deg,
                            {c1},
                            {c2}
                        );
                        padding:20px;
                        border-radius:15px;
                        margin-bottom:15px;
                        color:white;
                        font-size:20px;
                        font-weight:bold;
                    ">
                    📊 Cluster {cluster}: Average Customers
                    <br>
                    Stable customer group with
                    moderate spending behavior.
                    </div>
                    """,
                    unsafe_allow_html=True)

        # END OF TRY

    except Exception as e:

        st.error(
            f"Application Error: {e}"
        )

else:

    st.info(
        "Upload Mall_Customers.csv to begin analysis."
    )

# FOOTER
st.markdown("---")

st.caption(
    "🚀 CustomerIQ | Built by Tamil S | AIML"
)