
import flet as ft
import os, sys
import pprint
import subprocess
import time

sys.path.insert(0, os.path.dirname(__file__))

from models.database import Database
from models.user import User
from controllers.donor_controller import DonorController
from controllers.recipient_controller import RecipientController
from views.donor_view import donor_dashboard
from views.recipient_view import recipient_dashboard

def main(page: ft.Page):
    # --- Start FastAPI server if not running ---
    import socket
    def is_port_in_use(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("127.0.0.1", port)) == 0

    if not is_port_in_use(8000):
        # Start FastAPI server in background
        subprocess.Popen([
            sys.executable, "-m", "uvicorn", "api:app", "--reload"
        ], cwd=os.path.dirname(os.path.abspath(__file__)))
        # Wait a bit for the server to start
        for _ in range(10):
            if is_port_in_use(8000):
                break
            time.sleep(0.5)
    page.title = "Food Rescue Platform"
    db = Database()
    donor_ctrl = DonorController(db)
    recipient_ctrl = RecipientController(db)

    # --- Nav Buttons ---
    register_btn_nav = ft.ElevatedButton("Register", on_click=lambda _: show_register())
    login_btn_nav    = ft.ElevatedButton("Login",    on_click=lambda _: show_login())

    # --- Registration Fields ---
    reg_type_dd     = ft.Dropdown(options=[ft.dropdown.Option("donor"), ft.dropdown.Option("recipient")], label="Register as")
    reg_name_tf     = ft.TextField(label="Name")
    reg_contact_tf  = ft.TextField(label="Contact (optional)")
    reg_password_tf = ft.TextField(label="Password", password=True, can_reveal_password=True)
    reg_submit_btn  = ft.ElevatedButton("Submit Registration", on_click=lambda _: register_user())

    register_view = ft.Column([
        ft.Text("Register New Account", style="headlineSmall"),
        reg_type_dd, reg_name_tf, reg_contact_tf, reg_password_tf, reg_submit_btn
    ], visible=True)

    # --- Login Fields ---
    login_id_tf       = ft.TextField(label="Enter your user_id")
    login_password_tf = ft.TextField(label="Password", password=True, can_reveal_password=True)
    login_submit_btn  = ft.ElevatedButton("Submit Login", on_click=lambda _: login_user())

    login_view = ft.Column([
        ft.Text("Login to Existing Account", style="headlineSmall"),
        login_id_tf, login_password_tf, login_submit_btn
    ], visible=False)

    # --- UI Switchers ---
    def show_register():
        register_view.visible = True
        login_view.visible    = False
        rebuild_nav()

    def show_login():
        register_view.visible = False
        login_view.visible    = True
        rebuild_nav()

    def rebuild_nav():
        page.controls.clear()
        page.add(
            ft.Row([register_btn_nav, login_btn_nav]),
            register_view,
            login_view
        )
        page.update()

    # --- Handlers ---
    def register_user():
        if not reg_name_tf.value or not reg_type_dd.value or not reg_password_tf.value:
            page.snack_bar = ft.SnackBar(ft.Text("All fields required"))
            page.snack_bar.open = True
            page.update()
            return
        uid = db.users.count_documents({}) + 1
        u = User(uid, reg_name_tf.value, reg_type_dd.value,
                 reg_contact_tf.value, reg_password_tf.value)
        db.add_user(u.to_dict())
        page.snack_bar = ft.SnackBar(ft.Text(f"Registered! Your user ID is {uid}"))
        page.snack_bar.open = True
        page.update() 
        launch_dashboard(uid, u.user_type)

    def login_user():
        try:
            uid = int(login_id_tf.value)
        except:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid user_id"))
            page.snack_bar.open = True
            page.update()
            return
        doc = db.find_user(uid)
        if not doc or doc.get("password") != login_password_tf.value:
            page.snack_bar = ft.SnackBar(ft.Text("Wrong user_id or password"))
            page.snack_bar.open = True
            page.update()
            return
        page.snack_bar = ft.SnackBar(ft.Text(f"Logged in! Your user ID is {uid}"))
        page.snack_bar.open = True
        page.update()
        launch_dashboard(uid, doc["user_type"])

    def logout(e=None):
        show_register()

    def launch_dashboard(uid, utype):
        page.controls.clear()
        if utype == "donor":
            page.add(donor_dashboard(page, donor_ctrl, uid, logout))
        else:
            page.add(recipient_dashboard(page, recipient_ctrl, uid, logout))
        page.update()

    # --- Initial UI ---
    rebuild_nav()

ft.app(target=main)
