import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# EXCEL DATA SOURCE
# ============================================================

EXCEL_FILE = "Ecommerce_Hive_PowerBI_Data.xlsx"

if not os.path.exists(EXCEL_FILE):
    st.error(
        f"Excel file not found: {EXCEL_FILE}. "
        "Please keep the Excel file in the same folder as app.py."
    )
    st.stop()

# Read the Excel workbook generated from Hive analysis
summary = pd.read_excel(
    EXCEL_FILE,
    sheet_name="Summary"
)

monthly = pd.read_excel(
    EXCEL_FILE,
    sheet_name="Monthly Revenue"
)

products_revenue = pd.read_excel(
    EXCEL_FILE,
    sheet_name="Top Products Revenue"
)

products_quantity = pd.read_excel(
    EXCEL_FILE,
    sheet_name="Top Products Quantity"
)

country_revenue = pd.read_excel(
    EXCEL_FILE,
    sheet_name="Country Revenue"
)

country_records = pd.read_excel(
    EXCEL_FILE,
    sheet_name="Country Records"
)

# ============================================================
# STANDARDIZE COLUMN NAMES
# ============================================================

monthly = monthly.rename(columns={
    "Revenue (£)": "Revenue"
})

products_revenue = products_revenue.rename(columns={
    "Description": "Product",
    "Revenue (£)": "Revenue"
})

products_quantity = products_quantity.rename(columns={
    "Description": "Product",
    "Total Quantity": "Quantity"
})

country_revenue = country_revenue.rename(columns={
    "Revenue (£)": "Revenue"
})

country_records = country_records.rename(columns={
    "Line Item Records": "Records"
})

# ============================================================
# SUMMARY VALUES FROM EXCEL
# ============================================================

summary_values = dict(
    zip(
        summary["Metric"],
        summary["Value"]
    )
)

TOTAL_REVENUE = float(
    summary_values.get("Total Revenue (£)", 0)
)

COMPLETED_ORDERS = int(
    summary_values.get("Completed Orders", 0)
)

UNIQUE_CUSTOMERS = int(
    summary_values.get("Unique Customers", 0)
)

RETURNS = int(
    summary_values.get("Cancellation Line Items", 0)
)

VALID_RECORDS = int(
    summary_values.get("Valid Records", 0)
)

# ============================================================
# SESSION STATE
# ============================================================

if "selected_months" not in st.session_state:
    st.session_state.selected_months = monthly["Period"].tolist()

if "selected_countries" not in st.session_state:
    st.session_state.selected_countries = country_revenue["Country"].tolist()

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* Keep Streamlit header so the sidebar menu button remains visible */
[data-testid="stHeader"] {
    background: transparent;
}

/* Remove the extra top spacing left by the header */
[data-testid="stAppViewContainer"] > .main {
    padding-top: 0rem;
}

.stApp {
    background-color: #f4f7fb;
    color: #172033;
}

.block-container {
    max-width: 1450px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}

/* HEADER */

.topbar {
    background: white;
    border: 1px solid #dce3ed;
    border-radius: 16px;
    padding: 16px 22px;
    margin-bottom: 18px;
    box-shadow: 0 4px 14px rgba(20,30,50,0.06);
}

.brand {
    font-size: 21px;
    font-weight: 800;
    color: #172033;
}

.brand-small {
    font-size: 12px;
    color: #64748b;
    margin-top: 3px;
}

/* HERO */

.hero {
    background: linear-gradient(
        120deg,
        #4338ca,
        #6366f1,
        #7c3aed
    );
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 20px;
    box-shadow: 0 12px 30px rgba(79,70,229,0.22);
}

.hero-small {
    color: #dfe4ff;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1.4px;
    font-weight: 700;
}

.hero-title {
    color: white;
    font-size: 34px;
    font-weight: 800;
    margin-top: 6px;
}

.hero-text {
    color: #eef0ff;
    font-size: 14px;
    max-width: 850px;
    line-height: 1.6;
}

/* KPI */

.kpi {
    background: white;
    border: 1px solid #dce3ed;
    border-radius: 15px;
    padding: 20px;
    min-height: 125px;
    box-shadow: 0 4px 14px rgba(20,30,50,0.05);
}

.kpi-label {
    color: #64748b;
    font-size: 11px;
    text-transform: uppercase;
    font-weight: 800;
    letter-spacing: 0.8px;
}

.kpi-value {
    color: #111827;
    font-size: 27px;
    font-weight: 800;
    margin-top: 8px;
}

.kpi-note {
    color: #7b8799;
    font-size: 11px;
    margin-top: 4px;
}

/* SECTION */

.section-title {
    color: #172033;
    font-size: 22px;
    font-weight: 800;
    margin-top: 28px;
}

.section-subtitle {
    color: #64748b;
    font-size: 13px;
    margin-bottom: 12px;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: white;
    border-right: 1px solid #dce3ed;
}

[data-testid="stSidebar"] * {
    color: #172033 !important;
}

.sidebar-title {
    font-size: 21px;
    font-weight: 800;
    color: #172033 !important;
}

.sidebar-subtitle {
    color: #64748b !important;
    font-size: 12px;
    margin-bottom: 20px;
}

.filter-heading {
    color: #475569 !important;
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-top: 18px;
    margin-bottom: 8px;
}

/* BUTTONS */

div.stButton > button {
    background: white !important;
    color: #334155 !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 9px !important;
    font-weight: 700 !important;
}

div.stButton > button:hover {
    background: #eef2ff !important;
    color: #4338ca !important;
    border-color: #6366f1 !important;
}

/* CHECKBOX */

[data-testid="stCheckbox"] label {
    color: #334155 !important;
}

/* TABS */

.stTabs [data-baseweb="tab-list"] {
    background: white;
    border: 1px solid #dce3ed;
    border-radius: 12px;
    padding: 4px;
}

.stTabs [data-baseweb="tab"] {
    color: #475569 !important;
    font-weight: 700;
}

.stTabs [aria-selected="true"] {
    background: #eef2ff !important;
    color: #4338ca !important;
    border-radius: 8px;
}

/* CHART CONTAINER */

[data-testid="stPlotlyChart"] {
    background: white;
    border: 1px solid #dce3ed;
    border-radius: 15px;
    padding: 6px;
    box-shadow: 0 4px 14px rgba(20,30,50,0.05);
}

/* INFO BOX */

.filter-info {
    background: #eef2ff;
    border: 1px solid #c7d2fe;
    color: #3730a3;
    border-radius: 10px;
    padding: 12px 15px;
    margin: 12px 0 18px;
    font-size: 13px;
    font-weight: 600;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #94a3b8;
    border-top: 1px solid #dce3ed;
    margin-top: 35px;
    padding-top: 18px;
    font-size: 11px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🛍️ E-Commerce Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">Interactive dashboard controls</div>',
        unsafe_allow_html=True
    )

    # -----------------------------
    # MONTH FILTER
    # -----------------------------

    st.markdown(
        '<div class="filter-heading">Time Period</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✓ All Months"):
            st.session_state.selected_months = monthly["Period"].tolist()
            st.rerun()

    with col2:
        if st.button("Clear"):
            st.session_state.selected_months = []
            st.rerun()

    if st.button("⭐ Peak Months"):
        st.session_state.selected_months = [
            "2011-09",
            "2011-10",
            "2011-11"
        ]
        st.rerun()

    st.markdown(
        '<div class="filter-heading">Select Months</div>',
        unsafe_allow_html=True
    )

    new_months = []

    for month in monthly["Period"]:

        checked = st.checkbox(
            month,
            value=month in st.session_state.selected_months,
            key="month_" + month
        )

        if checked:
            new_months.append(month)

    st.session_state.selected_months = new_months

    # -----------------------------
    # COUNTRY FILTER
    # -----------------------------

    st.markdown(
        '<div class="filter-heading">Markets</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("All Markets"):
            st.session_state.selected_countries = (
                country_revenue["Country"].tolist()
            )
            st.rerun()

    with col2:
        if st.button("Top 5"):
            st.session_state.selected_countries = (
                country_revenue.head(5)["Country"].tolist()
            )
            st.rerun()

    new_countries = []

    for country in country_revenue["Country"]:

        checked = st.checkbox(
            country,
            value=country in st.session_state.selected_countries,
            key="country_" + country
        )

        if checked:
            new_countries.append(country)

    st.session_state.selected_countries = new_countries

    st.divider()

    st.markdown("### Project Stack")

    st.caption(
        "CSV → HDFS → Apache Hive → HiveQL → Excel → Streamlit"
    )

    st.caption(
        "Dashboard frontend runs locally on Windows."
    )

# ============================================================
# TOP HEADER
# ============================================================

st.markdown(
    '<div class="topbar">'
    '<div class="brand">🛍️ E-Commerce Analytics</div>'
    '<div class="brand-small">Apache Hive • Hadoop/HDFS • Streamlit Analytics</div>'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="hero">'
    '<div class="hero-small">E-Commerce Analytics Platform</div>'
    '<div class="hero-title">Business performance at a glance.</div>'
    '<div class="hero-text">'
    'Explore revenue trends, product performance and international '
    'markets using results generated from Apache Hive and Hadoop.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">Total Revenue</div>
            <div class="kpi-value">£{TOTAL_REVENUE:,.2f}</div>
            <div class="kpi-note">Total analysed revenue</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">Completed Orders</div>
            <div class="kpi-value">{COMPLETED_ORDERS:,}</div>
            <div class="kpi-note">Distinct non-cancelled invoices</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">Unique Customers</div>
            <div class="kpi-value">{UNIQUE_CUSTOMERS:,}</div>
            <div class="kpi-note">Distinct customer IDs</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">Returns / Cancellations</div>
            <div class="kpi-value">{RETURNS:,}</div>
            <div class="kpi-note">Cancellation line items</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# ACTIVE FILTER INFO
# ============================================================

selected_month_data = monthly[
    monthly["Period"].isin(
        st.session_state.selected_months
    )
]

selected_country_data = country_revenue[
    country_revenue["Country"].isin(
        st.session_state.selected_countries
    )
]

selected_revenue = selected_month_data["Revenue"].sum()

st.markdown(
    f"""
    <div class="filter-info">
        🔎 Active filters:
        {len(st.session_state.selected_months)} months
        &nbsp;•&nbsp;
        {len(st.session_state.selected_countries)} markets
        &nbsp;•&nbsp;
        Selected monthly revenue:
        £{selected_revenue:,.2f}
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# TABS
# ============================================================

tab_revenue, tab_products, tab_markets, tab_data = st.tabs([
    "📈 Revenue",
    "📦 Products",
    "🌍 Markets",
    "📋 Data"
])

# ============================================================
# PLOTLY STYLE FUNCTION
# ============================================================

def style_chart(fig, height=420):

    fig.update_layout(
        height=height,
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Arial",
            color="#172033",
            size=13
        ),
        margin=dict(
            l=30,
            r=30,
            t=25,
            b=35
        ),
        hoverlabel=dict(
            bgcolor="#172033",
            font_color="white",
            font_size=13
        )
    )

    fig.update_xaxes(
        color="#334155",
        title_font=dict(
            color="#172033",
            size=13
        ),
        tickfont=dict(
            color="#334155",
            size=12
        ),
        gridcolor="#dbe3ee",
        zerolinecolor="#cbd5e1"
    )

    fig.update_yaxes(
        color="#334155",
        title_font=dict(
            color="#172033",
            size=13
        ),
        tickfont=dict(
            color="#334155",
            size=12
        ),
        gridcolor="#dbe3ee",
        zerolinecolor="#cbd5e1"
    )

    return fig


# ============================================================
# REVENUE TAB
# ============================================================

with tab_revenue:

    st.markdown(
        '<div class="section-title">Revenue Performance</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Monthly revenue trend based on your selected time period.'
        '</div>',
        unsafe_allow_html=True
    )

    if selected_month_data.empty:

        st.warning(
            "Please select at least one month from the sidebar."
        )

    else:

        col1, col2 = st.columns([1.6, 1])

        # -------------------------
        # LINE CHART
        # -------------------------

        with col1:

            fig = px.line(
                selected_month_data,
                x="Period",
                y="Revenue",
                markers=True
            )

            fig.update_traces(
                line=dict(
                    color="#4f46e5",
                    width=4
                ),
                marker=dict(
                    size=10,
                    color="#f97316",
                    line=dict(
                        color="white",
                        width=2
                    )
                )
            )

            fig.update_yaxes(
                tickprefix="£",
                tickformat=",.0f"
            )

            st.plotly_chart(
                style_chart(fig, 420),
                width="stretch"
            )

        # -------------------------
        # BAR CHART
        # -------------------------

        with col2:

            fig = px.bar(
                selected_month_data,
                x="Period",
                y="Revenue",
                color="Revenue",
                color_continuous_scale=[
                    "#c7d2fe",
                    "#6366f1",
                    "#4338ca"
                ],
                text="Revenue"
            )

            fig.update_traces(
                texttemplate="£%{y:,.0f}",
                textposition="outside",
                textfont=dict(
                    color="#172033",
                    size=11
                )
            )

            fig.update_coloraxes(
                showscale=False
            )

            fig.update_yaxes(
                tickprefix="£",
                tickformat=",.0f"
            )

            st.plotly_chart(
                style_chart(fig, 420),
                width="stretch"
            )

        # -------------------------
        # RANKING
        # -------------------------

        st.markdown(
            '<div class="section-title">Monthly Revenue Ranking</div>',
            unsafe_allow_html=True
        )

        ranked = selected_month_data.sort_values(
            "Revenue",
            ascending=True
        )

        fig = px.bar(
            ranked,
            x="Revenue",
            y="Period",
            orientation="h",
            color="Revenue",
            color_continuous_scale=[
                "#bfdbfe",
                "#3b82f6",
                "#4338ca"
            ],
            text="Revenue"
        )

        fig.update_traces(
            texttemplate="£%{x:,.0f}",
            textposition="outside",
            textfont=dict(
                color="#172033",
                size=12
            )
        )

        fig.update_coloraxes(
            showscale=False
        )

        fig.update_xaxes(
            tickprefix="£",
            tickformat=",.0f"
        )

        st.plotly_chart(
            style_chart(fig, 400),
            width="stretch"
        )

# ============================================================
# PRODUCTS TAB
# ============================================================

with tab_products:

    st.markdown(
        '<div class="section-title">Product Performance</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Top products identified from the completed Hive analysis.'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Product charts show the Top 10 Hive analysis results. "
        "The month and market filters affect Revenue and Market charts, "
        "not these pre-computed Top 10 product rankings."
    )

    col1, col2 = st.columns(2)

    # -------------------------
    # REVENUE PRODUCTS
    # -------------------------

    with col1:

        data = products_revenue.sort_values(
            "Revenue",
            ascending=True
        )

        fig = px.bar(
            data,
            x="Revenue",
            y="Product",
            orientation="h",
            color="Revenue",
            color_continuous_scale=[
                "#ddd6fe",
                "#8b5cf6",
                "#6d28d9"
            ],
            text="Revenue"
        )

        fig.update_traces(
            texttemplate="£%{x:,.0f}",
            textposition="outside",
            textfont=dict(
                color="#172033",
                size=12
            )
        )

        fig.update_coloraxes(
            showscale=False
        )

        fig.update_xaxes(
            tickprefix="£",
            tickformat=",.0f"
        )

        st.plotly_chart(
            style_chart(fig, 520),
            width="stretch"
        )

    # -------------------------
    # QUANTITY PRODUCTS
    # -------------------------

    with col2:

        data = products_quantity.sort_values(
            "Quantity",
            ascending=True
        )

        fig = px.bar(
            data,
            x="Quantity",
            y="Product",
            orientation="h",
            color="Quantity",
            color_continuous_scale=[
                "#a7f3d0",
                "#10b981",
                "#047857"
            ],
            text="Quantity"
        )

        fig.update_traces(
            texttemplate="%{x:,}",
            textposition="outside",
            textfont=dict(
                color="#172033",
                size=12
            )
        )

        fig.update_coloraxes(
            showscale=False
        )

        fig.update_xaxes(
            tickformat=","
        )

        st.plotly_chart(
            style_chart(fig, 520),
            width="stretch"
        )

    # -------------------------
    # PRODUCT SCATTER
    # -------------------------

    st.markdown(
        '<div class="section-title">Revenue vs Quantity</div>',
        unsafe_allow_html=True
    )

    product_compare = products_revenue.merge(
        products_quantity[
            ["Stock Code", "Quantity"]
        ],
        on="Stock Code",
        how="left"
    )

    fig = px.scatter(
        product_compare,
        x="Quantity",
        y="Revenue",
        size="Revenue",
        color="Revenue",
        hover_name="Product",
        text="Stock Code",
        color_continuous_scale=[
            "#fef3c7",
            "#f97316",
            "#db2777"
        ]
    )

    fig.update_traces(
        textposition="top center",
        textfont=dict(
            color="#172033",
            size=11
        )
    )

    fig.update_coloraxes(
        showscale=False
    )

    fig.update_yaxes(
        tickprefix="£",
        tickformat=",.0f"
    )

    st.plotly_chart(
        style_chart(fig, 440),
        width="stretch"
    )

# ============================================================
# MARKETS TAB
# ============================================================

with tab_markets:

    st.markdown(
        '<div class="section-title">Market Performance</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Revenue and line-item activity by country.'
        '</div>',
        unsafe_allow_html=True
    )

    if selected_country_data.empty:

        st.warning(
            "Please select at least one market from the sidebar."
        )

    else:

        col1, col2 = st.columns([1.5, 1])

        # -------------------------
        # COUNTRY REVENUE
        # -------------------------

        with col1:

            data = selected_country_data.sort_values(
                "Revenue",
                ascending=True
            )

            fig = px.bar(
                data,
                x="Revenue",
                y="Country",
                orientation="h",
                color="Revenue",
                color_continuous_scale=[
                    "#bae6fd",
                    "#06b6d4",
                    "#2563eb"
                ],
                text="Revenue"
            )

            fig.update_traces(
                texttemplate="£%{x:,.0f}",
                textposition="outside",
                textfont=dict(
                    color="#172033",
                    size=12
                )
            )

            fig.update_coloraxes(
                showscale=False
            )

            fig.update_xaxes(
                tickprefix="£",
                tickformat=",.0f"
            )

            st.plotly_chart(
                style_chart(fig, 470),
                width="stretch"
            )

        # -------------------------
        # PIE
        # -------------------------

        with col2:

            pie_data = selected_country_data.copy()

            if len(pie_data) > 6:

                top = pie_data.nlargest(
                    5,
                    "Revenue"
                )

                other_value = (
                    pie_data["Revenue"].sum()
                    - top["Revenue"].sum()
                )

                other = pd.DataFrame({
                    "Country": ["Other"],
                    "Revenue": [other_value]
                })

                pie_data = pd.concat(
                    [top, other],
                    ignore_index=True
                )

            fig = px.pie(
                pie_data,
                names="Country",
                values="Revenue",
                hole=0.48,
                color_discrete_sequence=[
                    "#4338ca",
                    "#06b6d4",
                    "#10b981",
                    "#f59e0b",
                    "#ef4444",
                    "#94a3b8"
                ]
            )

            fig.update_traces(
                textinfo="percent+label",
                textfont=dict(
                    color="#172033",
                    size=12
                )
            )

            st.plotly_chart(
                style_chart(fig, 470),
                width="stretch"
            )

        # -------------------------
        # RECORD COUNTS
        # -------------------------

        st.markdown(
            '<div class="section-title">Transaction Activity</div>',
            unsafe_allow_html=True
        )

        selected_records = country_records[
            country_records["Country"].isin(
                st.session_state.selected_countries
            )
        ]

        data = selected_records.sort_values(
            "Records",
            ascending=True
        )

        fig = px.bar(
            data,
            x="Records",
            y="Country",
            orientation="h",
            color="Records",
            color_continuous_scale=[
                "#fed7aa",
                "#fb923c",
                "#ea580c"
            ],
            text="Records"
        )

        fig.update_traces(
            texttemplate="%{x:,}",
            textposition="outside",
            textfont=dict(
                color="#172033",
                size=12
            )
        )

        fig.update_coloraxes(
            showscale=False
        )

        fig.update_xaxes(
            tickformat=","
        )

        st.plotly_chart(
            style_chart(fig, 420),
            width="stretch"
        )

        st.caption(
            "Country record counts represent line-item records, "
            "not distinct orders."
        )

# ============================================================
# DATA TAB
# ============================================================

with tab_data:

    st.markdown(
        '<div class="section-title">Analysis Tables</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Result tables generated from the Hive analysis.'
        '</div>',
        unsafe_allow_html=True
    )

    table1, table2, table3 = st.tabs([
        "Monthly Revenue",
        "Products",
        "Countries"
    ])

    # MONTHLY TABLE

    with table1:

        data = selected_month_data.copy()

        data["Revenue"] = data["Revenue"].apply(
            lambda x: f"£{x:,.2f}"
        )

        st.dataframe(
            data,
            width="stretch",
            hide_index=True
        )

    # PRODUCT TABLES

    with table2:

        st.subheader("Top Products by Revenue")

        data = products_revenue.copy()

        data["Revenue"] = data["Revenue"].apply(
            lambda x: f"£{x:,.2f}"
        )

        st.dataframe(
            data,
            width="stretch",
            hide_index=True
        )

        st.subheader("Top Products by Quantity")

        data = products_quantity.copy()

        data["Quantity"] = data["Quantity"].apply(
            lambda x: f"{x:,}"
        )

        st.dataframe(
            data,
            width="stretch",
            hide_index=True
        )

    # COUNTRY TABLES

    with table3:

        st.subheader("Country Revenue")

        data = selected_country_data.copy()

        data["Revenue"] = data["Revenue"].apply(
            lambda x: f"£{x:,.2f}"
        )

        st.dataframe(
            data,
            width="stretch",
            hide_index=True
        )

        st.subheader("Country Records")

        data = country_records[
            country_records["Country"].isin(
                st.session_state.selected_countries
            )
        ].copy()

        data["Records"] = data["Records"].apply(
            lambda x: f"{x:,}"
        )

        st.dataframe(
            data,
            width="stretch",
            hide_index=True
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    E-Commerce Customer & Product Analysis
    &nbsp;•&nbsp;
    Apache Hadoop
    &nbsp;•&nbsp;
    Apache Hive
    &nbsp;•&nbsp;
    Streamlit
</div>
""", unsafe_allow_html=True)