"""
================================================================================
FOUNDATIONS OF DATA SCIENCE (25ITC31) - EXPLORATORY DATA ANALYSIS (EDA)
PROJECT: Public Transport Management and Passenger Travel Analysis System
INSTITUTION: Velalar College of Engineering and Technology, Erode - 12
DEPARTMENT: Information Technology
STUDENT: Jeffrin | REGISTER NUMBER: 732925ITR040 | CLASS: 25IT3A
================================================================================
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set overall style for publication quality graphics
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.titlesize": 16,
    "figure.dpi": 300
})

# Define output directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "public_transport_dataset.csv")
VIZ_DIRS = [
    os.path.join(BASE_DIR, "visualizations"),
    os.path.join(BASE_DIR, "..", "src", "main", "resources", "static", "visualizations")
]

for vdir in VIZ_DIRS:
    os.makedirs(vdir, exist_ok=True)

print("[INFO] Starting Data Science & Visualizations Pipeline...")
print(f"[INFO] Ingesting dataset from: {DATA_PATH}")

# ------------------------------------------------------------------------------
# STEP 1: DATA INGESTION & EXPLORATION (Unit 1 & Unit 2)
# ------------------------------------------------------------------------------
df = pd.read_csv(DATA_PATH)
print(f"[INFO] Dataset loaded successfully. Shape: {df.shape[0]} rows, {df.shape[1]} columns.")
print("\n--- SAMPLE DATA PREVIEW (First 3 rows) ---")
print(df.head(3)[["booking_id", "route_name", "bus_type", "total_amount", "booking_status"]])

# ------------------------------------------------------------------------------
# STEP 2: DATA CLEANING & TRANSFORMATION (Unit 3 & Unit 4)
# ------------------------------------------------------------------------------
print("\n[INFO] Checking for missing values:")
print(df.isnull().sum())

# Ensure proper data types
df["booking_timestamp"] = pd.to_datetime(df["booking_timestamp"])
df["travel_date"] = pd.to_datetime(df["travel_date"])
df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce")
df["occupancy_rate_pct"] = pd.to_numeric(df["occupancy_rate_pct"], errors="coerce")

# Feature Engineering
df["booking_day_of_week"] = df["booking_timestamp"].dt.day_name()
df["booking_date_only"] = df["booking_timestamp"].dt.date
df["departure_hour"] = pd.to_datetime(df["departure_time"], format="%H:%M").dt.hour

# Summary Statistics (Unit 1: Averages, Variance, Std Deviation)
print("\n--- DESCRIPTIVE STATISTICS (Numeric Attributes) ---")
print(df[["distance_km", "fare_per_seat", "seats_booked", "total_amount", "occupancy_rate_pct"]].describe().T)

def save_plot_dual(fig, filename):
    for vdir in VIZ_DIRS:
        out_path = os.path.join(vdir, filename)
        fig.savefig(out_path, bbox_inches="tight", dpi=300)
    print(f"[SUCCESS] Saved chart: {filename}")
    plt.close(fig)

# ------------------------------------------------------------------------------
# VISUALIZATION 1: Route-Wise Passenger Demand (Bar Chart)
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
route_demand = df[df["booking_status"] == "CONFIRMED"].groupby("route_name")["seats_booked"].sum().sort_values(ascending=False)
sns.barplot(x=route_demand.values, y=route_demand.index, palette="Blues_r", ax=ax)
ax.set_title("Route-Wise Passenger Travel Demand (VCET Corridor Analysis)", weight="bold", pad=15)
ax.set_xlabel("Total Confirmed Passengers (Seats Booked)")
ax.set_ylabel("Transit Corridor")
for i, v in enumerate(route_demand.values):
    ax.text(v + 1, i, str(int(v)), va="center", fontweight="bold", color="#1f2937")
save_plot_dual(fig, "01_route_wise_passenger_demand.png")

# ------------------------------------------------------------------------------
# VISUALIZATION 2: Route-Wise Revenue Generation (Bar Chart)
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
route_revenue = df[df["booking_status"] == "CONFIRMED"].groupby("route_name")["total_amount"].sum().sort_values(ascending=False)
sns.barplot(x=route_revenue.values, y=route_revenue.index, palette="Greens_r", ax=ax)
ax.set_title("Gross Revenue by Transit Route (in INR ₹)", weight="bold", pad=15)
ax.set_xlabel("Total Revenue (₹)")
ax.set_ylabel("Transit Corridor")
for i, v in enumerate(route_revenue.values):
    ax.text(v + 200, i, f"₹{v:,.0f}", va="center", fontweight="bold", color="#064e3b")
save_plot_dual(fig, "02_route_wise_revenue.png")

# ------------------------------------------------------------------------------
# VISUALIZATION 3: Seat Occupancy Rate Distribution by Bus Type (Box Plot)
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 6))
sns.boxplot(x="bus_type", y="occupancy_rate_pct", data=df, palette="Set2", ax=ax, width=0.5)
sns.stripplot(x="bus_type", y="occupancy_rate_pct", data=df, color="black", alpha=0.3, jitter=0.2, ax=ax)
ax.set_title("Bus Seat Occupancy Rate Distribution Across Fleet Categories", weight="bold", pad=15)
ax.set_xlabel("Bus Category")
ax.set_ylabel("Seat Occupancy Rate (%)")
ax.axhline(df["occupancy_rate_pct"].mean(), color="red", linestyle="--", label=f"Average Occupancy ({df['occupancy_rate_pct'].mean():.1f}%)")
ax.legend(loc="lower right")
save_plot_dual(fig, "03_bus_type_occupancy_distribution.png")

# ------------------------------------------------------------------------------
# VISUALIZATION 4: Hourly Departure Pattern & Peak Commute Profile (Histogram & KDE)
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(df["departure_hour"], bins=24, kde=True, color="#4f46e5", ax=ax)
ax.set_title("Hourly Schedule Departure Distribution (Peak Commute Profile)", weight="bold", pad=15)
ax.set_xlabel("Departure Hour (24-Hour Military Format)")
ax.set_ylabel("Number of Trip Departures")
ax.set_xticks(range(0, 24, 2))
save_plot_dual(fig, "04_hourly_departure_pattern.png")

# ------------------------------------------------------------------------------
# VISUALIZATION 5: Booking Status Ratio (Pie / Donut Chart)
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 7))
status_counts = df["booking_status"].value_counts()
colors = ["#10b981", "#ef4444"]
wedges, texts, autotexts = ax.pie(
    status_counts.values, 
    labels=status_counts.index, 
    autopct="%1.1f%%", 
    startangle=140, 
    colors=colors, 
    wedgeprops=dict(width=0.45, edgecolor="w", linewidth=2)
)
for autotext in autotexts:
    autotext.set_fontsize(12)
    autotext.set_fontweight("bold")
ax.set_title("Ticket Booking Health: Confirmed vs. Cancelled Ratio", weight="bold", pad=20)
save_plot_dual(fig, "05_booking_status_distribution.png")

# ------------------------------------------------------------------------------
# VISUALIZATION 6: Correlation Heatmap of Travel Metrics
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6))
numeric_cols = ["distance_km", "fare_per_seat", "seats_booked", "total_amount", "occupancy_rate_pct", "passenger_age"]
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, cbar_kws={"shrink": 0.8}, ax=ax)
ax.set_title("Correlation Matrix of Transit Key Performance Indicators", weight="bold", pad=15)
save_plot_dual(fig, "06_correlation_heatmap.png")

# ------------------------------------------------------------------------------
# VISUALIZATION 7: Daily Booking Trends Over Time (Time Series Line Chart)
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 5))
daily_bookings = df.groupby("booking_date_only")["seats_booked"].sum()
ax.plot(daily_bookings.index, daily_bookings.values, marker="o", color="#0284c7", linewidth=2.5, markersize=6)
ax.fill_between(daily_bookings.index, daily_bookings.values, color="#38bdf8", alpha=0.25)
ax.set_title("Daily Passenger Booking Trend (Time Series Demand)", weight="bold", pad=15)
ax.set_xlabel("Booking Date")
ax.set_ylabel("Total Confirmed Bookings (Seats)")
plt.xticks(rotation=45)
save_plot_dual(fig, "07_daily_booking_trends.png")

print("\n[COMPLETE] All 7 data science visualizations generated and exported successfully!")
