import io
import matplotlib.pyplot as plt
import flet as ft

# Example analytics view for food saved, donor participation, and delivery efficiency
def analytics_view(page, db):
    # --- Data fetching (replace with real queries) ---
    # --- Actual Data ---
    import datetime
    from collections import defaultdict

    # Get all food items from DB
    food_items = list(db.food_items.find())

    # Group by month (YYYY-MM)
    month_stats = defaultdict(lambda: {"food_saved": 0, "donors": set(), "deliveries": 0, "claimed": 0})
    for item in food_items:
        # Parse expiry_date or fallback to 'Unknown'
        try:
            dt = datetime.datetime.strptime(item.get("expiry_date", ""), "%Y-%m-%d")
            month = dt.strftime("%b %Y")
        except Exception:
            month = "Unknown"
        month_stats[month]["food_saved"] += int(item.get("quantity", 0))
        month_stats[month]["donors"].add(item.get("donor_id"))
        month_stats[month]["deliveries"] += 1
        if item.get("is_claimed"):
            month_stats[month]["claimed"] += 1

    # Sort months chronologically (skip 'Unknown')
    months = sorted([m for m in month_stats if m != "Unknown"], key=lambda x: datetime.datetime.strptime(x, "%b %Y"))
    if not months:
        months = ["No Data"]

    food_saved = [month_stats[m]["food_saved"] for m in months]
    donors = [len(month_stats[m]["donors"]) for m in months]
    deliveries = [month_stats[m]["deliveries"] for m in months]
    efficiency = [round((month_stats[m]["claimed"] / month_stats[m]["deliveries"] * 100) if month_stats[m]["deliveries"] else 0, 2) for m in months]

    # --- Food Saved Chart ---
    fig1, ax1 = plt.subplots()
    ax1.plot(months, food_saved, marker='o')
    ax1.set_title('Food Saved Over Time')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Food Saved (kg)')
    buf1 = io.BytesIO()
    fig1.savefig(buf1, format='png')
    plt.close(fig1)
    buf1.seek(0)

    # --- Donor Participation Chart ---
    fig2, ax2 = plt.subplots()
    ax2.bar(months, donors)
    ax2.set_title('Donor Participation')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Number of Donors')
    buf2 = io.BytesIO()
    fig2.savefig(buf2, format='png')
    plt.close(fig2)
    buf2.seek(0)

    # --- Delivery Efficiency Chart ---
    fig3, ax3 = plt.subplots()
    ax3.plot(months, efficiency, color='green', marker='s')
    ax3.set_title('Delivery Efficiency')
    ax3.set_xlabel('Month')
    ax3.set_ylabel('Efficiency (%)')
    buf3 = io.BytesIO()
    fig3.savefig(buf3, format='png')
    plt.close(fig3)
    buf3.seek(0)

    import base64
    img1 = ft.Image(src_base64=base64.b64encode(buf1.getvalue()).decode(), width=400, height=300)
    img2 = ft.Image(src_base64=base64.b64encode(buf2.getvalue()).decode(), width=400, height=300)
    img3 = ft.Image(src_base64=base64.b64encode(buf3.getvalue()).decode(), width=400, height=300)

    return ft.Container(
        content=ft.Column([
            ft.Text("Analytics Dashboard", style="headlineMedium"),
            ft.Text("Food Saved Over Time"), img1,
            ft.Text("Donor Participation"), img2,
            ft.Text("Delivery Efficiency"), img3,
            ft.ElevatedButton("Back", on_click=lambda e: page.go_back())
        ], scroll="auto"),
        height=600  # Adjust as needed for your app window
    )
