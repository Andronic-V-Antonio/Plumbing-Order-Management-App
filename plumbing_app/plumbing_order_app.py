import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys


# ============================================================
# DEMO PLUMBING ITEMS
# ============================================================

DEMO_ITEMS = [
    {
        "id": "PL001",
        "description": "32mm Sink Waste",
        "category": "Waste"
    },
    {
        "id": "PL002",
        "description": "40mm Sink Waste",
        "category": "Waste"
    },
    {
        "id": "PL003",
        "description": "Flexible Tap Connector",
        "category": "Tap"
    },
    {
        "id": "PL004",
        "description": "15mm Copper Pipe",
        "category": "Pipe"
    },
    {
        "id": "PL005",
        "description": "15mm Elbow",
        "category": "Fitting"
    },
    {
        "id": "PL006",
        "description": "15mm Tee",
        "category": "Fitting"
    },
    {
        "id": "PL007",
        "description": "Isolation Valve",
        "category": "Valve"
    },
    {
        "id": "PL008",
        "description": "PTFE Tape",
        "category": "Consumable"
    },
    {
        "id": "PL009",
        "description": "Basin Tap",
        "category": "Tap"
    },
    {
        "id": "PL010",
        "description": "Sink Trap",
        "category": "Waste"
    }
]


# ============================================================
# MAIN APPLICATION
# ============================================================

class PlumbingApp:

    def __init__(self, root):

        self.root = root

        self.root.title("CBM Plumbing Order Manager")
        self.root.geometry("1050x700")
        self.root.minsize(900, 600)

        # ----------------------------------------------------
        # COLOURS
        # ----------------------------------------------------

        self.cb_blue = "#1769AA"

        self.root.configure(
            bg="white"
        )

        # ----------------------------------------------------
        # DATA
        # ----------------------------------------------------

        self.orders = {}

        self.next_order_number = 1

        self.current_order = []

        # ----------------------------------------------------
        # DATA FILE LOCATION
        # ----------------------------------------------------

        # When running the .py file:
        # save orders beside the Python file.
        #
        # When running the .exe:
        # save orders beside the .exe.

        if getattr(sys, "frozen", False):

            app_folder = os.path.dirname(
                sys.executable
            )

        else:

            app_folder = os.path.dirname(
                os.path.abspath(__file__)
            )

        self.data_file = os.path.join(
            app_folder,
            "orders.json"
        )

        # ----------------------------------------------------
        # LOAD SAVED ORDERS
        # ----------------------------------------------------

        self.load_orders()

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        self.create_header()

        # ----------------------------------------------------
        # NOTEBOOK
        # ----------------------------------------------------

        self.notebook = ttk.Notebook(
            self.root
        )

        self.notebook.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        # ----------------------------------------------------
        # CREATE TABS
        # ----------------------------------------------------

        self.create_order_tab()

        self.create_delivery_tab()

        self.create_messages_tab()

        # ----------------------------------------------------
        # REFRESH DROPDOWNS
        # ----------------------------------------------------

        self.refresh_order_dropdowns()


    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg=self.cb_blue,
            height=75
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )

        # CBM LOGO

        logo = tk.Label(
            header,
            text="CBM",
            font=("Arial", 28, "bold"),
            bg=self.cb_blue,
            fg="white"
        )

        logo.pack(
            side="left",
            padx=(25, 15)
        )

        # TITLE

        title_frame = tk.Frame(
            header,
            bg=self.cb_blue
        )

        title_frame.pack(
            side="left",
            fill="y"
        )

        title = tk.Label(
            title_frame,
            text="Plumbing Order Manager",
            font=("Arial", 20, "bold"),
            bg=self.cb_blue,
            fg="white"
        )

        title.pack(
            anchor="w",
            pady=(13, 0)
        )

        subtitle = tk.Label(
            title_frame,
            text="Order preparation and delivery checking",
            font=("Arial", 10),
            bg=self.cb_blue,
            fg="white"
        )

        subtitle.pack(
            anchor="w"
        )


    # ========================================================
    # CREATE ORDER TAB
    # ========================================================

    def create_order_tab(self):

        self.order_tab = ttk.Frame(
            self.notebook
        )

        self.notebook.add(
            self.order_tab,
            text="Create Order"
        )

        # ----------------------------------------------------
        # SITE / JOB
        # ----------------------------------------------------

        top_frame = tk.Frame(
            self.order_tab,
            bg="white"
        )

        top_frame.pack(
            fill="x",
            padx=15,
            pady=15
        )

        tk.Label(
            top_frame,
            text="Site / Job:",
            font=("Arial", 11, "bold"),
            bg="white"
        ).pack(
            side="left"
        )

        self.site_entry = tk.Entry(
            top_frame,
            font=("Arial", 11),
            width=35
        )

        self.site_entry.pack(
            side="left",
            padx=10
        )

        # ----------------------------------------------------
        # AVAILABLE ITEMS
        # ----------------------------------------------------

        item_frame = tk.LabelFrame(
            self.order_tab,
            text="Available Plumbing Items",
            font=("Arial", 11, "bold"),
            bg="white"
        )

        item_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 10)
        )

        columns = (
            "id",
            "description",
            "category"
        )

        self.item_tree = ttk.Treeview(
            item_frame,
            columns=columns,
            show="headings",
            height=10
        )

        self.item_tree.heading(
            "id",
            text="Item ID"
        )

        self.item_tree.heading(
            "description",
            text="Description"
        )

        self.item_tree.heading(
            "category",
            text="Category"
        )

        self.item_tree.column(
            "id",
            width=100
        )

        self.item_tree.column(
            "description",
            width=300
        )

        self.item_tree.column(
            "category",
            width=150
        )

        self.item_tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        scrollbar = ttk.Scrollbar(
            item_frame,
            orient="vertical",
            command=self.item_tree.yview
        )

        scrollbar.pack(
            side="right",
            fill="y",
            pady=10
        )

        self.item_tree.configure(
            yscrollcommand=scrollbar.set
        )

        # ADD DEMO ITEMS

        for item in DEMO_ITEMS:

            self.item_tree.insert(
                "",
                "end",
                iid=item["id"],
                values=(
                    item["id"],
                    item["description"],
                    item["category"]
                )
            )

        # ----------------------------------------------------
        # QUANTITY AND ITEM BUTTONS
        # ----------------------------------------------------

        quantity_frame = tk.Frame(
            self.order_tab,
            bg="white"
        )

        quantity_frame.pack(
            fill="x",
            padx=15,
            pady=5
        )

        tk.Label(
            quantity_frame,
            text="Quantity:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).pack(
            side="left"
        )

        self.quantity_var = tk.StringVar(
            value="1"
        )

        self.quantity_spinbox = tk.Spinbox(
            quantity_frame,
            from_=1,
            to=999,
            textvariable=self.quantity_var,
            width=8
        )

        self.quantity_spinbox.pack(
            side="left",
            padx=10
        )

        # ADD ITEM

        tk.Button(
            quantity_frame,
            text="ADD ITEM",
            command=self.add_item,
            bg=self.cb_blue,
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15
        ).pack(
            side="left",
            padx=5
        )

        # REMOVE

        tk.Button(
            quantity_frame,
            text="REMOVE SELECTED",
            command=self.remove_item,
            padx=15
        ).pack(
            side="left",
            padx=5
        )

        # CLEAR

        tk.Button(
            quantity_frame,
            text="CLEAR ORDER",
            command=self.clear_order,
            padx=15
        ).pack(
            side="left",
            padx=5
        )

        # ----------------------------------------------------
        # CURRENT ORDER
        # ----------------------------------------------------

        current_frame = tk.LabelFrame(
            self.order_tab,
            text="Current Order",
            font=("Arial", 11, "bold"),
            bg="white"
        )

        current_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        order_columns = (
            "id",
            "description",
            "quantity"
        )

        self.current_order_tree = ttk.Treeview(
            current_frame,
            columns=order_columns,
            show="headings",
            height=5
        )

        self.current_order_tree.heading(
            "id",
            text="Item ID"
        )

        self.current_order_tree.heading(
            "description",
            text="Description"
        )

        self.current_order_tree.heading(
            "quantity",
            text="Quantity"
        )

        self.current_order_tree.column(
            "id",
            width=100
        )

        self.current_order_tree.column(
            "description",
            width=350
        )

        self.current_order_tree.column(
            "quantity",
            width=100
        )

        self.current_order_tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ----------------------------------------------------
        # CREATE ORDER BUTTON
        # ----------------------------------------------------

        create_frame = tk.Frame(
            self.order_tab,
            bg="white"
        )

        create_frame.pack(
            fill="x",
            padx=15,
            pady=15
        )

        create_button = tk.Button(
            create_frame,
            text="CREATE ORDER",
            command=self.create_order,
            bg=self.cb_blue,
            fg="white",
            activebackground="#0D4F80",
            activeforeground="white",
            font=("Arial", 13, "bold"),
            padx=40,
            pady=12,
            cursor="hand2"
        )

        create_button.pack(
            side="right"
        )


    # ========================================================
    # ADD ITEM
    # ========================================================

    def add_item(self):

        selected = self.item_tree.selection()

        if not selected:

            messagebox.showwarning(
                "No Item Selected",
                "Please select a plumbing item first."
            )

            return

        item_id = selected[0]

        try:

            quantity = int(
                self.quantity_var.get()
            )

            if quantity <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Quantity",
                "Please enter a valid quantity."
            )

            return

        item = next(
            (
                x for x in DEMO_ITEMS
                if x["id"] == item_id
            ),
            None
        )

        if item is None:
            return

        # CHECK IF ITEM ALREADY EXISTS

        existing = next(
            (
                x for x in self.current_order
                if x["id"] == item_id
            ),
            None
        )

        if existing:

            existing["quantity"] += quantity

        else:

            self.current_order.append(
                {
                    "id": item["id"],
                    "description": item["description"],
                    "category": item["category"],
                    "quantity": quantity
                }
            )

        self.refresh_current_order()


    # ========================================================
    # REMOVE ITEM
    # ========================================================

    def remove_item(self):

        selected = self.current_order_tree.selection()

        if not selected:

            messagebox.showwarning(
                "No Item Selected",
                "Please select an item from the current order."
            )

            return

        item_id = selected[0]

        self.current_order = [
            item
            for item in self.current_order
            if item["id"] != item_id
        ]

        self.refresh_current_order()


    # ========================================================
    # CLEAR ORDER
    # ========================================================

    def clear_order(self):

        self.current_order = []

        self.refresh_current_order()


    # ========================================================
    # REFRESH CURRENT ORDER
    # ========================================================

    def refresh_current_order(self):

        for item in self.current_order_tree.get_children():

            self.current_order_tree.delete(
                item
            )

        for item in self.current_order:

            self.current_order_tree.insert(
                "",
                "end",
                iid=item["id"],
                values=(
                    item["id"],
                    item["description"],
                    item["quantity"]
                )
            )


    # ========================================================
    # CREATE ORDER
    # ========================================================

    def create_order(self):

        if not self.current_order:

            messagebox.showwarning(
                "Empty Order",
                "Please add at least one item."
            )

            return

        site = self.site_entry.get().strip()

        if not site:

            site = "Not specified"

        order_id = (
            f"ORD-{self.next_order_number:03d}"
        )

        order_items = []

        for item in self.current_order:

            order_items.append(
                {
                    "id": item["id"],
                    "description": item["description"],
                    "category": item["category"],
                    "quantity": item["quantity"],
                    "status": "Not Checked"
                }
            )

        self.orders[order_id] = {
            "site": site,
            "items": order_items
        }

        self.next_order_number += 1

        self.save_orders()

        messagebox.showinfo(
            "Order Created",
            f"Order {order_id} has been created successfully."
        )

        # CLEAR CURRENT ORDER

        self.current_order = []

        self.refresh_current_order()

        self.site_entry.delete(
            0,
            tk.END
        )

        # REFRESH DROPDOWNS

        self.refresh_order_dropdowns()

        self.delivery_order_var.set(
            order_id
        )

        self.message_order_var.set(
            order_id
        )

        self.refresh_delivery()

        self.generate_order_message()


    # ========================================================
    # DELIVERY TAB
    # ========================================================

    def create_delivery_tab(self):

        self.delivery_tab = ttk.Frame(
            self.notebook
        )

        self.notebook.add(
            self.delivery_tab,
            text="Check Delivery"
        )

        # ----------------------------------------------------
        # SELECT ORDER
        # ----------------------------------------------------

        select_frame = tk.Frame(
            self.delivery_tab,
            bg="white"
        )

        select_frame.pack(
            fill="x",
            padx=15,
            pady=15
        )

        tk.Label(
            select_frame,
            text="Select Order:",
            font=("Arial", 11, "bold"),
            bg="white"
        ).pack(
            side="left"
        )

        self.delivery_order_var = tk.StringVar()

        self.delivery_order_combo = ttk.Combobox(
            select_frame,
            textvariable=self.delivery_order_var,
            state="readonly",
            width=20
        )

        self.delivery_order_combo.pack(
            side="left",
            padx=10
        )

        self.delivery_order_combo.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_delivery()
        )

        # SITE

        self.delivery_site_label = tk.Label(
            select_frame,
            text="Site: -",
            font=("Arial", 10),
            bg="white"
        )

        self.delivery_site_label.pack(
            side="left",
            padx=20
        )

        # ----------------------------------------------------
        # DELIVERY TABLE
        # ----------------------------------------------------

        delivery_frame = tk.LabelFrame(
            self.delivery_tab,
            text="Delivery Checklist",
            font=("Arial", 11, "bold"),
            bg="white"
        )

        delivery_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=5
        )

        delivery_columns = (
            "id",
            "description",
            "quantity",
            "status"
        )

        self.delivery_tree = ttk.Treeview(
            delivery_frame,
            columns=delivery_columns,
            show="headings"
        )

        self.delivery_tree.heading(
            "id",
            text="Item ID"
        )

        self.delivery_tree.heading(
            "description",
            text="Description"
        )

        self.delivery_tree.heading(
            "quantity",
            text="Quantity"
        )

        self.delivery_tree.heading(
            "status",
            text="Status"
        )

        self.delivery_tree.column(
            "id",
            width=100
        )

        self.delivery_tree.column(
            "description",
            width=350
        )

        self.delivery_tree.column(
            "quantity",
            width=100
        )

        self.delivery_tree.column(
            "status",
            width=150
        )

        self.delivery_tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ----------------------------------------------------
        # STATUS BUTTONS
        # ----------------------------------------------------

        status_frame = tk.Frame(
            self.delivery_tab,
            bg="white"
        )

        status_frame.pack(
            fill="x",
            padx=15,
            pady=10
        )

        tk.Button(
            status_frame,
            text="HAVE",
            command=lambda: self.set_delivery_status("Have"),
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            status_frame,
            text="MISSING",
            command=lambda: self.set_delivery_status("Missing"),
            bg="#D9534F",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            status_frame,
            text="NOT CHECKED",
            command=lambda: self.set_delivery_status("Not Checked"),
            width=12
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            status_frame,
            text="REFRESH",
            command=self.refresh_delivery,
            width=12
        ).pack(
            side="right",
            padx=5
        )


    # ========================================================
    # REFRESH DELIVERY
    # ========================================================

    def refresh_delivery(self):

        for item in self.delivery_tree.get_children():

            self.delivery_tree.delete(
                item
            )

        order_id = self.delivery_order_var.get()

        if not order_id:

            self.delivery_site_label.config(
                text="Site: -"
            )

            return

        if order_id not in self.orders:

            self.delivery_site_label.config(
                text="Site: -"
            )

            return

        order = self.orders[order_id]

        self.delivery_site_label.config(
            text=f"Site: {order.get('site', 'Not specified')}"
        )

        for item in order["items"]:

            self.delivery_tree.insert(
                "",
                "end",
                iid=item["id"],
                values=(
                    item["id"],
                    item["description"],
                    item["quantity"],
                    item.get(
                        "status",
                        "Not Checked"
                    )
                )
            )


    # ========================================================
    # SET DELIVERY STATUS
    # ========================================================

    def set_delivery_status(self, status):

        selected = self.delivery_tree.selection()

        if not selected:

            messagebox.showwarning(
                "No Item Selected",
                "Please select an item first."
            )

            return

        order_id = self.delivery_order_var.get()

        if not order_id:
            return

        selected_id = selected[0]

        for item in self.orders[order_id]["items"]:

            if item["id"] == selected_id:

                item["status"] = status

                break

        self.save_orders()

        self.refresh_delivery()


    # ========================================================
    # MESSAGES TAB
    # ========================================================

    def create_messages_tab(self):

        self.messages_tab = ttk.Frame(
            self.notebook
        )

        self.notebook.add(
            self.messages_tab,
            text="Messages"
        )

        # ----------------------------------------------------
        # SELECT ORDER
        # ----------------------------------------------------

        select_frame = tk.Frame(
            self.messages_tab,
            bg="white"
        )

        select_frame.pack(
            fill="x",
            padx=15,
            pady=15
        )

        tk.Label(
            select_frame,
            text="Select Order:",
            font=("Arial", 11, "bold"),
            bg="white"
        ).pack(
            side="left"
        )

        self.message_order_var = tk.StringVar()

        self.message_order_combo = ttk.Combobox(
            select_frame,
            textvariable=self.message_order_var,
            state="readonly",
            width=20
        )

        self.message_order_combo.pack(
            side="left",
            padx=10
        )

        self.message_order_combo.bind(
            "<<ComboboxSelected>>",
            lambda event: self.generate_order_message()
        )

        # ----------------------------------------------------
        # MESSAGE BUTTONS
        # ----------------------------------------------------

        button_frame = tk.Frame(
            self.messages_tab,
            bg="white"
        )

        button_frame.pack(
            fill="x",
            padx=15,
            pady=5
        )

        tk.Button(
            button_frame,
            text="ORDER EMAIL",
            command=self.generate_order_message,
            bg=self.cb_blue,
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="MISSING ITEMS EMAIL",
            command=self.generate_missing_message,
            bg="#D9534F",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="COPY EMAIL",
            command=self.copy_message,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="DELETE SELECTED ORDER",
            command=self.delete_selected_order,
            padx=15
        ).pack(
            side="right",
            padx=5
        )

        # ----------------------------------------------------
        # EMAIL EDITOR
        # ----------------------------------------------------

        editor_frame = tk.LabelFrame(
            self.messages_tab,
            text="Email Editor",
            font=("Arial", 11, "bold"),
            bg="white"
        )

        editor_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.message_text = tk.Text(
            editor_frame,
            wrap="word",
            font=("Arial", 11)
        )

        self.message_text.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


    # ========================================================
    # GENERATE ORDER EMAIL
    # ========================================================

    def generate_order_message(self):

        order_id = self.message_order_var.get()

        if not order_id:
            return

        if order_id not in self.orders:
            return

        order = self.orders[order_id]

        site = order.get(
            "site",
            "Not specified"
        )

        message = []

        message.append(
            f"Subject: Plumbing Order - {order_id}"
        )

        message.append("")

        message.append(
            "Hello,"
        )

        message.append("")

        message.append(
            f"Please could you arrange the following plumbing materials for {site}."
        )

        message.append("")

        message.append(
            f"Order ID: {order_id}"
        )

        message.append("")

        for item in order["items"]:

            message.append(
                f"- {item['description']} - Quantity: {item['quantity']}"
            )

        message.append("")

        message.append(
            "Please confirm once the order has been arranged."
        )

        message.append("")

        message.append(
            "Thanks,"
        )

        message.append(
            "CBM"
        )

        final_message = "\n".join(
            message
        )

        self.message_text.delete(
            "1.0",
            tk.END
        )

        self.message_text.insert(
            "1.0",
            final_message
        )


    # ========================================================
    # GENERATE MISSING ITEMS EMAIL
    # ========================================================

    def generate_missing_message(self):

        order_id = self.message_order_var.get()

        if not order_id:
            return

        if order_id not in self.orders:
            return

        order = self.orders[order_id]

        site = order.get(
            "site",
            "Not specified"
        )

        missing_items = [
            item
            for item in order["items"]
            if item.get("status") == "Missing"
        ]

        if not missing_items:

            messagebox.showinfo(
                "No Missing Items",
                "There are currently no items marked as missing for this order."
            )

            return

        message = []

        message.append(
            f"Subject: Missing Plumbing Items - {order_id}"
        )

        message.append("")

        message.append(
            "Hello,"
        )

        message.append("")

        message.append(
            f"The following plumbing items are missing from delivery for {site}."
        )

        message.append("")

        message.append(
            f"Order ID: {order_id}"
        )

        message.append("")

        for item in missing_items:

            message.append(
                f"- {item['description']} - Quantity: {item['quantity']}"
            )

        message.append("")

        message.append(
            "Please could you arrange the missing items."
        )

        message.append("")

        message.append(
            "Thanks,"
        )

        message.append(
            "CBM"
        )

        final_message = "\n".join(
            message
        )

        self.message_text.delete(
            "1.0",
            tk.END
        )

        self.message_text.insert(
            "1.0",
            final_message
        )


    # ========================================================
    # COPY EMAIL
    # ========================================================

    def copy_message(self):

        message = self.message_text.get(
            "1.0",
            tk.END
        ).strip()

        if not message:

            messagebox.showwarning(
                "No Message",
                "There is no message to copy."
            )

            return

        self.root.clipboard_clear()

        self.root.clipboard_append(
            message
        )

        self.root.update()

        messagebox.showinfo(
            "Copied",
            "Email copied to clipboard."
        )


    # ========================================================
    # DELETE ORDER
    # ========================================================

    def delete_selected_order(self):

        order_id = self.message_order_var.get()

        if not order_id:

            messagebox.showwarning(
                "No Order Selected",
                "Please select an order first."
            )

            return

        if order_id not in self.orders:
            return

        answer = messagebox.askyesno(
            "Delete Order",
            f"Are you sure you want to delete {order_id}?"
        )

        if not answer:
            return

        del self.orders[order_id]

        self.save_orders()

        self.message_text.delete(
            "1.0",
            tk.END
        )

        self.refresh_order_dropdowns()

        messagebox.showinfo(
            "Order Deleted",
            f"{order_id} has been deleted."
        )


    # ========================================================
    # REFRESH ORDER DROPDOWNS
    # ========================================================

    def refresh_order_dropdowns(self):

        order_ids = list(
            self.orders.keys()
        )

        self.delivery_order_combo["values"] = order_ids

        self.message_order_combo["values"] = order_ids

        # DELIVERY

        current_delivery = (
            self.delivery_order_var.get()
        )

        if current_delivery in order_ids:

            self.delivery_order_var.set(
                current_delivery
            )

        elif order_ids:

            self.delivery_order_var.set(
                order_ids[-1]
            )

        else:

            self.delivery_order_var.set("")

        # MESSAGES

        current_message = (
            self.message_order_var.get()
        )

        if current_message in order_ids:

            self.message_order_var.set(
                current_message
            )

        elif order_ids:

            self.message_order_var.set(
                order_ids[-1]
            )

        else:

            self.message_order_var.set("")

        self.refresh_delivery()


    # ========================================================
    # SAVE ORDERS
    # ========================================================

    def save_orders(self):

        data = {
            "next_order_number": self.next_order_number,
            "orders": self.orders
        }

        try:

            with open(
                self.data_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4
                )

        except Exception as error:

            messagebox.showerror(
                "Save Error",
                f"Could not save orders.\n\n{error}"
            )


    # ========================================================
    # LOAD ORDERS
    # ========================================================

    def load_orders(self):

        if not os.path.exists(
            self.data_file
        ):

            return

        try:

            with open(
                self.data_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(
                    file
                )

            self.orders = data.get(
                "orders",
                {}
            )

            self.next_order_number = data.get(
                "next_order_number",
                1
            )

            # Make sure the next Order ID
            # is higher than existing orders.

            highest_number = 0

            for order_id in self.orders.keys():

                try:

                    number = int(
                        order_id.replace(
                            "ORD-",
                            ""
                        )
                    )

                    if number > highest_number:

                        highest_number = number

                except ValueError:

                    pass

            if self.next_order_number <= highest_number:

                self.next_order_number = (
                    highest_number + 1
                )

        except Exception as error:

            messagebox.showwarning(
                "Load Warning",
                f"Saved orders could not be loaded.\n\n{error}"
            )

            self.orders = {}

            self.next_order_number = 1


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = PlumbingApp(
        root
    )

    root.mainloop()