import flet as ft

def recipient_dashboard(page, recipient_controller, recipient_id, on_logout):
    # Label showing who is logged in
    user_id_label = ft.Text(f"Logged in as Recipient ID: {recipient_id}", weight="bold")

    # Lists for available and claimed items
    available_food_list = ft.ListView(expand=1, spacing=10, padding=10)
    claimed_food_list   = ft.ListView(expand=1, spacing=10, padding=10)

    # Handler to refresh available items
    def refresh_available_food(e):
        available_food_list.controls.clear()
        foods = recipient_controller.list_available_food()
        for item in foods:
            claim_btn = ft.ElevatedButton(
                "Claim",
                on_click=lambda e, fid=item["item_id"]: claim_food(e, fid)
            )
            available_food_list.controls.append(
                ft.Row(
                    [
                        ft.Text(
                            f"{item['name']} ({item['quantity']}) "
                            f"DonorID: {item['donor_id']} Exp: {item['expiry_date']} | Location: {item.get('location', 'N/A')}"
                        ),
                        claim_btn
                    ]
                )
            )
        page.update()

    # Handler to refresh claimed items
    def refresh_claimed_food(e):
        claimed_food_list.controls.clear()
        claimed = recipient_controller.list_claimed_food(recipient_id)
        for item in claimed:
            claimed_food_list.controls.append(
                ft.Text(
                    f"{item['name']} ({item['quantity']}) - "
                    f"Claimed Exp: {item['expiry_date']} | Location: {item.get('location', 'N/A')}"
                )
            )
        page.update()

    # Handler to claim an item
    def claim_food(e, food_id):
        recipient_controller.claim_food(food_id, recipient_id)
        page.snack_bar = ft.SnackBar(ft.Text("Food claimed!"))
        page.snack_bar.open = True
        refresh_available_food(None)
        refresh_claimed_food(None)

    # Analytics button
    from views.analytics_view import analytics_view
    def show_analytics(e):
        page.controls.clear()
        page.add(analytics_view(page, recipient_controller.db))
        page.update()

    # Logout button
    logout_btn = ft.ElevatedButton("Logout", on_click=on_logout)
    analytics_btn = ft.ElevatedButton("Analytics", on_click=show_analytics)

    # Build and return the dashboard
    return ft.Column(
        [
            user_id_label,
            ft.Text("Recipient Dashboard", style="headlineSmall"),
            ft.Row([logout_btn, analytics_btn]),
            ft.ElevatedButton("Refresh Food List", on_click=refresh_available_food),
            ft.Text("Available Food:", weight="bold"),
            available_food_list,
            ft.Divider(),
            ft.ElevatedButton("Show My Claimed Food", on_click=refresh_claimed_food),
            ft.Text("Your Claimed Food:", weight="bold"),
            claimed_food_list
        ]
    )
