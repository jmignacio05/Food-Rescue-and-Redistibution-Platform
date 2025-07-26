import flet as ft

def donor_dashboard(page, donor_controller, donor_id, on_logout):
    # Label showing who is logged in
    user_id_label = ft.Text(f"Logged in as Donor ID: {donor_id}", weight="bold")

    # Input fields
    food_name_tf   = ft.TextField(label="Food Name")
    food_qty_tf    = ft.TextField(label="Quantity")
    food_expiry_tf = ft.TextField(label="Expiry Date (YYYY-MM-DD)")
    food_location_tf = ft.TextField(label="Pickup Location (Where can food be claimed?)")

    # List of this donor’s posted items
    donor_food_list = ft.ListView(expand=1, spacing=10, padding=10)

    # Handler to post new food
    def post_food(e):
        donor_controller.post_food(
            donor_id=donor_id,
            name=food_name_tf.value,
            quantity=food_qty_tf.value,
            expiry_date=food_expiry_tf.value,
            location=food_location_tf.value
        )
        food_name_tf.value   = ""
        food_qty_tf.value    = ""
        food_expiry_tf.value = ""
        food_location_tf.value = ""
        page.snack_bar = ft.SnackBar(ft.Text("Food posted!"))
        page.snack_bar.open = True
        show_my_food(None)

    # Handler to refresh the list
    def show_my_food(e):
        donor_food_list.controls.clear()
        foods = donor_controller.view_my_food(donor_id)
        for item in foods:
            status = "Claimed" if item["is_claimed"] else "Available"
            donor_food_list.controls.append(
                ft.Text(
                    f"{item['name']} ({item['quantity']}) - "
                    f"{status} Exp: {item['expiry_date']} | Location: {item.get('location', 'N/A')}"
                )
            )
        page.update()

    # Analytics button
    from views.analytics_view import analytics_view
    def show_analytics(e):
        page.controls.clear()
        page.add(analytics_view(page, donor_controller.db))
        page.update()

    # Logout button
    logout_btn = ft.ElevatedButton("Logout", on_click=on_logout)
    analytics_btn = ft.ElevatedButton("Analytics", on_click=show_analytics)

    # Build and return the dashboard
    return ft.Column([
        user_id_label,
        ft.Text("Donor Dashboard", style="headlineSmall"),
        ft.Row([logout_btn, analytics_btn]),
        food_name_tf,
        food_qty_tf,
        food_expiry_tf,
        food_location_tf,
        ft.Row([
            ft.ElevatedButton("Post Food", on_click=post_food),
            ft.ElevatedButton("Refresh",   on_click=show_my_food)
        ]),
        ft.Text("Your Posted Food:", weight="bold"),
        donor_food_list
    ])
