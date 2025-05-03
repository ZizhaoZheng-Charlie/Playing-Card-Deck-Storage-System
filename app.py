import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import io
import webbrowser
from models import Session, Item, Series, WishItem


class ItemDetailsWindow(tk.Toplevel):
    def __init__(self, parent, item, item_type="inventory"):
        super().__init__(parent)
        self.item = item
        self.item_type = item_type

        if item_type == "inventory":
            self.title(f"Item Details: {item.name}")
        else:
            self.title(f"Wishlist Item Details: {item.name}")

        self.geometry("600x500")

        # Make window modal
        self.transient(parent)
        self.grab_set()

        self.setup_ui()

    def setup_ui(self):
        # Create main frame
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Create scrollable frame for all details
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Item details content
        row = 0

        # Common fields for both inventory and wishlist items
        ttk.Label(scrollable_frame, text="Name:", font=("", 10, "bold")).grid(
            row=row, column=0, sticky="w", padx=5, pady=5
        )
        ttk.Label(scrollable_frame, text=self.item.name).grid(
            row=row, column=1, sticky="w", padx=5, pady=5
        )
        row += 1

        if self.item.series:
            ttk.Label(scrollable_frame, text="Series:", font=("", 10, "bold")).grid(
                row=row, column=0, sticky="w", padx=5, pady=5
            )
            ttk.Label(scrollable_frame, text=self.item.series.name).grid(
                row=row, column=1, sticky="w", padx=5, pady=5
            )
            row += 1

            ttk.Label(scrollable_frame, text="Company:", font=("", 10, "bold")).grid(
                row=row, column=0, sticky="w", padx=5, pady=5
            )
            ttk.Label(
                scrollable_frame, text=self.item.series.company_name or "N/A"
            ).grid(row=row, column=1, sticky="w", padx=5, pady=5)
            row += 1

            ttk.Label(
                scrollable_frame, text="Shop Website:", font=("", 10, "bold")
            ).grid(row=row, column=0, sticky="w", padx=5, pady=5)

            if self.item.series.shop_website:
                url_frame = ttk.Frame(scrollable_frame)
                url_frame.grid(row=row, column=1, sticky="w", padx=5, pady=5)

                ttk.Label(url_frame, text=self.item.series.shop_website).pack(
                    side="left", padx=(0, 10)
                )

                def open_series_url():
                    url = self.item.series.shop_website
                    if not url.startswith(("http://", "https://")):
                        url = "https://" + url
                    webbrowser.open(url)

                ttk.Button(url_frame, text="Visit", command=open_series_url).pack(
                    side="left"
                )
            else:
                ttk.Label(scrollable_frame, text="N/A").grid(
                    row=row, column=1, sticky="w", padx=5, pady=5
                )

            row += 1

        # Status fields
        ttk.Label(scrollable_frame, text="Signature:", font=("", 10, "bold")).grid(
            row=row, column=0, sticky="w", padx=5, pady=5
        )
        ttk.Label(
            scrollable_frame, text="Yes" if self.item.is_signature else "No"
        ).grid(row=row, column=1, sticky="w", padx=5, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Gilded:", font=("", 10, "bold")).grid(
            row=row, column=0, sticky="w", padx=5, pady=5
        )
        ttk.Label(scrollable_frame, text="Yes" if self.item.is_gilded else "No").grid(
            row=row, column=1, sticky="w", padx=5, pady=5
        )
        row += 1

        ttk.Label(scrollable_frame, text="Sealed:", font=("", 10, "bold")).grid(
            row=row, column=0, sticky="w", padx=5, pady=5
        )
        ttk.Label(scrollable_frame, text="Yes" if self.item.is_sealed else "No").grid(
            row=row, column=1, sticky="w", padx=5, pady=5
        )
        row += 1

        # Fields specific to inventory items
        if self.item_type == "inventory":
            ttk.Label(scrollable_frame, text="Quantity:", font=("", 10, "bold")).grid(
                row=row, column=0, sticky="w", padx=5, pady=5
            )
            ttk.Label(scrollable_frame, text=str(self.item.quantity)).grid(
                row=row, column=1, sticky="w", padx=5, pady=5
            )
            row += 1

            ttk.Label(scrollable_frame, text="Image:", font=("", 10, "bold")).grid(
                row=row, column=0, sticky="w", padx=5, pady=5
            )
            if self.item.image_name:
                ttk.Label(scrollable_frame, text=self.item.image_name).grid(
                    row=row, column=1, sticky="w", padx=5, pady=5
                )
            else:
                ttk.Label(scrollable_frame, text="No image").grid(
                    row=row, column=1, sticky="w", padx=5, pady=5
                )
            row += 1

            # Display image if available
            if self.item.image:
                try:
                    img = Image.open(io.BytesIO(self.item.image))
                    img.thumbnail((300, 300))
                    photo = ImageTk.PhotoImage(img)

                    img_frame = ttk.Frame(scrollable_frame)
                    img_frame.grid(row=row, column=0, columnspan=2, pady=10)

                    img_label = ttk.Label(img_frame, image=photo)
                    img_label.image = photo  # Keep a reference
                    img_label.pack()

                    row += 1
                except Exception as e:
                    print(f"Error loading image: {e}")

        # Fields specific to wishlist items
        else:
            ttk.Label(
                scrollable_frame, text="Expected Price:", font=("", 10, "bold")
            ).grid(row=row, column=0, sticky="w", padx=5, pady=5)
            ttk.Label(scrollable_frame, text=self.item.expected_price or "N/A").grid(
                row=row, column=1, sticky="w", padx=5, pady=5
            )
            row += 1

            ttk.Label(scrollable_frame, text="Priority:", font=("", 10, "bold")).grid(
                row=row, column=0, sticky="w", padx=5, pady=5
            )
            ttk.Label(scrollable_frame, text=self.item.priority).grid(
                row=row, column=1, sticky="w", padx=5, pady=5
            )
            row += 1

            ttk.Label(scrollable_frame, text="Shop URL:", font=("", 10, "bold")).grid(
                row=row, column=0, sticky="w", padx=5, pady=5
            )

            if self.item.shop_url:
                url_frame = ttk.Frame(scrollable_frame)
                url_frame.grid(row=row, column=1, sticky="w", padx=5, pady=5)

                ttk.Label(url_frame, text=self.item.shop_url).pack(
                    side="left", padx=(0, 10)
                )

                def open_shop_url():
                    url = self.item.shop_url
                    if not url.startswith(("http://", "https://")):
                        url = "https://" + url
                    webbrowser.open(url)

                ttk.Button(url_frame, text="Visit", command=open_shop_url).pack(
                    side="left"
                )
            else:
                ttk.Label(scrollable_frame, text="N/A").grid(
                    row=row, column=1, sticky="w", padx=5, pady=5
                )

            row += 1

            # Notes section
            ttk.Label(scrollable_frame, text="Notes:", font=("", 10, "bold")).grid(
                row=row, column=0, sticky="nw", padx=5, pady=5
            )

            notes_frame = ttk.Frame(scrollable_frame)
            notes_frame.grid(row=row, column=1, sticky="w", padx=5, pady=5)

            notes_text = tk.Text(notes_frame, wrap="word", width=40, height=6)
            notes_text.insert(
                "1.0", self.item.notes if self.item.notes else "No notes available."
            )
            notes_text.config(state="disabled")
            notes_text.pack()

            row += 1

        # Close button at bottom
        ttk.Button(self, text="Close", command=self.destroy).pack(pady=10)


class SeriesWindow(tk.Toplevel):
    def __init__(self, parent, session, callback=None):
        super().__init__(parent)
        self.title("Add New Series")
        self.geometry("400x300")

        self.session = session
        self.callback = callback

        # Make window modal
        self.transient(parent)
        self.grab_set()

        self.setup_ui()

    def setup_ui(self):
        # Create input fields
        ttk.Label(self, text="Series Name:").pack(pady=5)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(fill="x", padx=20, pady=5)

        ttk.Label(self, text="Shop Website:").pack(pady=5)
        self.website_entry = ttk.Entry(self)
        self.website_entry.pack(fill="x", padx=20, pady=5)

        ttk.Label(self, text="Company Name:").pack(pady=5)
        self.company_entry = ttk.Entry(self)
        self.company_entry.pack(fill="x", padx=20, pady=5)

        # Add button
        ttk.Button(self, text="Add Series", command=self.add_series).pack(pady=20)

    def add_series(self):
        name = self.name_entry.get().strip()
        website = self.website_entry.get().strip()
        company = self.company_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Series name is required!", parent=self)
            return

        new_series = Series(name=name, shop_website=website, company_name=company)

        self.session.add(new_series)
        self.session.commit()

        if self.callback:
            self.callback()

        messagebox.showinfo("Success", "Series added successfully!", parent=self)
        self.destroy()


class SeriesManageWindow(tk.Toplevel):
    def __init__(self, parent, session, refresh_callback=None):
        super().__init__(parent)
        self.title("Manage Series")
        self.geometry("600x400")

        self.session = session
        self.refresh_callback = refresh_callback

        # Make window modal
        self.transient(parent)
        self.grab_set()

        self.setup_ui()
        self.load_series()

    def setup_ui(self):
        # Create the treeview
        columns = ("id", "name", "company", "website")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        # Define headings
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Series Name")
        self.tree.heading("company", text="Company")
        self.tree.heading("website", text="Website")

        # Column widths
        self.tree.column("id", width=50)
        self.tree.column("name", width=150)
        self.tree.column("company", width=150)
        self.tree.column("website", width=200)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons frame
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_series).pack(
            side="left", padx=5
        )
        ttk.Button(btn_frame, text="Open Website", command=self.open_website).pack(
            side="left", padx=5
        )
        ttk.Button(btn_frame, text="Close", command=self.destroy).pack(
            side="right", padx=5
        )

        # Bind double-click to open website
        self.tree.bind("<Double-1>", lambda e: self.open_website())

    def load_series(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load series from database
        series_list = self.session.query(Series).all()
        for series in series_list:
            self.tree.insert(
                "",
                "end",
                values=(
                    series.id,
                    series.name,
                    series.company_name or "",
                    series.shop_website or "",
                ),
            )

    def delete_series(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Warning", "Please select a series to delete!", parent=self
            )
            return

        series_id = self.tree.item(selected[0])["values"][0]
        series = self.session.query(Series).get(series_id)

        # Check if series has items
        item_count = self.session.query(Item).filter_by(series_id=series_id).count()

        if item_count > 0:
            if not messagebox.askyesno(
                "Warning",
                f"This series has {item_count} items. Deleting it will delete all associated items. Continue?",
                parent=self,
            ):
                return

            # Delete all items in this series
            self.session.query(Item).filter_by(series_id=series_id).delete()

        # Delete the series
        self.session.delete(series)
        self.session.commit()

        self.load_series()

        if self.refresh_callback:
            self.refresh_callback()

        messagebox.showinfo("Success", "Series deleted successfully!", parent=self)

    def open_website(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Warning", "Please select a series to view website!", parent=self
            )
            return

        series_id = self.tree.item(selected[0])["values"][0]
        series = self.session.query(Series).get(series_id)

        if series and series.shop_website:
            url = series.shop_website
            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            webbrowser.open(url)
        else:
            messagebox.showinfo(
                "Info", "No website available for this series.", parent=self
            )


class WishItemWindow(tk.Toplevel):
    def __init__(self, parent, session, callback=None):
        super().__init__(parent)
        self.title("Add Wish Item")
        self.geometry("500x400")

        self.session = session
        self.callback = callback

        # Make window modal
        self.transient(parent)
        self.grab_set()

        self.setup_ui()
        self.refresh_series_list()

    def setup_ui(self):
        # Create input fields
        input_frame = ttk.Frame(self, padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Item Name:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.name_entry = ttk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Series:").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        self.series_combobox = ttk.Combobox(input_frame, state="readonly", width=28)
        self.series_combobox.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(
            input_frame, text="Add New Series", command=self.open_series_window
        ).grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(input_frame, text="Expected Price:").grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )
        self.price_entry = ttk.Entry(input_frame, width=30)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Shop URL:").grid(
            row=3, column=0, padx=5, pady=5, sticky="w"
        )
        self.url_entry = ttk.Entry(input_frame, width=30)
        self.url_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Notes:").grid(
            row=4, column=0, padx=5, pady=5, sticky="w"
        )
        self.notes_text = tk.Text(input_frame, width=30, height=4)
        self.notes_text.grid(row=4, column=1, padx=5, pady=5)

        # Priority dropdown
        ttk.Label(input_frame, text="Priority:").grid(
            row=5, column=0, padx=5, pady=5, sticky="w"
        )
        self.priority_combobox = ttk.Combobox(
            input_frame, values=["Low", "Medium", "High"], state="readonly", width=28
        )
        self.priority_combobox.current(1)  # Default to Medium
        self.priority_combobox.grid(row=5, column=1, padx=5, pady=5)

        # Checkbox for special features
        checkbox_frame = ttk.Frame(input_frame)
        checkbox_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        self.is_signature_var = tk.BooleanVar(value=False)
        self.is_gilded_var = tk.BooleanVar(value=False)
        self.is_sealed_var = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            checkbox_frame, text="Signature", variable=self.is_signature_var
        ).pack(side="left", padx=10)
        ttk.Checkbutton(
            checkbox_frame, text="Gilded", variable=self.is_gilded_var
        ).pack(side="left", padx=10)
        ttk.Checkbutton(
            checkbox_frame, text="Sealed", variable=self.is_sealed_var
        ).pack(side="left", padx=10)

        # Add button at bottom
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=15)

        ttk.Button(btn_frame, text="Add to Wishlist", command=self.add_wish_item).pack(
            side="right", padx=10
        )
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(
            side="right", padx=10
        )

    def open_series_window(self):
        SeriesWindow(self, self.session, callback=self.refresh_series_list)

    def refresh_series_list(self):
        series_list = self.session.query(Series).all()
        self.series_combobox["values"] = [s.name for s in series_list]
        if series_list:
            self.series_combobox.set(series_list[0].name)

    def add_wish_item(self):
        name = self.name_entry.get().strip()
        series_name = self.series_combobox.get()
        price = self.price_entry.get().strip()
        url = self.url_entry.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()
        priority = self.priority_combobox.get()

        if not name:
            messagebox.showerror("Error", "Item name is required!", parent=self)
            return

        if not series_name:
            messagebox.showerror("Error", "Please select or add a series!", parent=self)
            return

        series = self.session.query(Series).filter_by(name=series_name).first()

        # Get checkbox values
        is_signature = self.is_signature_var.get()
        is_gilded = self.is_gilded_var.get()
        is_sealed = self.is_sealed_var.get()

        # Create new wish item
        new_wish = WishItem(
            name=name,
            series=series,
            expected_price=price,
            shop_url=url,
            notes=notes,
            priority=priority,
            is_signature=is_signature,
            is_gilded=is_gilded,
            is_sealed=is_sealed,
        )

        self.session.add(new_wish)
        self.session.commit()

        if self.callback:
            self.callback()

        messagebox.showinfo(
            "Success", "Item added to wishlist successfully!", parent=self
        )
        self.destroy()


class ItemEditWindow(tk.Toplevel):
    def __init__(self, parent, session, item, callback=None):
        super().__init__(parent)
        self.title("Edit Item")
        self.geometry("500x400")

        self.session = session
        self.item = item
        self.callback = callback
        self.selected_image_path = None

        # Make window modal
        self.transient(parent)
        self.grab_set()

        self.setup_ui()
        self.load_item_data()

    def setup_ui(self):
        # Create input fields
        input_frame = ttk.Frame(self, padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Name:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.name_entry = ttk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Series:").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        self.series_combobox = ttk.Combobox(input_frame, state="readonly", width=28)
        self.series_combobox.grid(row=1, column=1, padx=5, pady=5)

        # Load series data
        series_list = self.session.query(Series).all()
        self.series_combobox["values"] = [s.name for s in series_list]

        ttk.Label(input_frame, text="Quantity:").grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )
        self.quantity_entry = ttk.Entry(input_frame, width=30)
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=5)

        # Image selection
        ttk.Label(input_frame, text="Image:").grid(
            row=3, column=0, padx=5, pady=5, sticky="w"
        )
        image_frame = ttk.Frame(input_frame)
        image_frame.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.image_label = ttk.Label(image_frame)
        self.image_label.pack(side="left", padx=(0, 10))

        self.image_button = ttk.Button(
            image_frame, text="Select New Image", command=self.select_image
        )
        self.image_button.pack(side="left")

        # Checkboxes for item status
        checkbox_frame = ttk.Frame(input_frame)
        checkbox_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # Create variables for checkboxes
        self.is_signature_var = tk.BooleanVar(value=False)
        self.is_gilded_var = tk.BooleanVar(value=False)
        self.is_sealed_var = tk.BooleanVar(value=False)

        # Create checkboxes
        ttk.Checkbutton(
            checkbox_frame, text="Signature", variable=self.is_signature_var
        ).pack(side="left", padx=10)

        ttk.Checkbutton(
            checkbox_frame, text="Gilded", variable=self.is_gilded_var
        ).pack(side="left", padx=10)

        ttk.Checkbutton(
            checkbox_frame, text="Sealed", variable=self.is_sealed_var
        ).pack(side="left", padx=10)

        # Preview frame for image
        preview_frame = ttk.LabelFrame(self, text="Image Preview", padding=10)
        preview_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.preview_label = ttk.Label(preview_frame)
        self.preview_label.pack(expand=True)

        # Button frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Save Changes", command=self.save_changes).pack(
            side="right", padx=5
        )
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(
            side="right", padx=5
        )

    def load_item_data(self):
        # Set entry values from item
        self.name_entry.insert(0, self.item.name)
        self.quantity_entry.insert(0, str(self.item.quantity))

        # Set series selection
        if self.item.series:
            self.series_combobox.set(self.item.series.name)

        # Set checkbox values
        self.is_signature_var.set(bool(self.item.is_signature))
        self.is_gilded_var.set(bool(self.item.is_gilded))
        self.is_sealed_var.set(bool(self.item.is_sealed))

        # Show image preview if available
        if self.item.image:
            self.show_preview(image_data=self.item.image)
            if self.item.image_name:
                self.image_label.config(text=f"Current: {self.item.image_name}")

    def select_image(self):
        self.selected_image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if self.selected_image_path:
            self.image_button.configure(text="Image Selected")
            self.image_label.config(
                text=f"New: {self.selected_image_path.split('/')[-1]}"
            )
            self.show_preview(self.selected_image_path)

    def show_preview(self, image_path=None, image_data=None):
        try:
            if image_path:
                image = Image.open(image_path)
            elif image_data:
                image = Image.open(io.BytesIO(image_data))
            else:
                self.preview_label.configure(image="")
                return

            # Resize image to fit preview (max 300x300)
            image.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(image)
            self.current_image = photo  # Keep a reference!
            self.preview_label.configure(image=photo)
        except Exception as e:
            print(f"Error showing preview: {e}")
            self.preview_label.configure(image="")

    def save_changes(self):
        # Get values from form
        name = self.name_entry.get().strip()
        series_name = self.series_combobox.get()
        quantity_str = self.quantity_entry.get().strip()

        # Validate
        if not name:
            messagebox.showerror("Error", "Name is required!", parent=self)
            return

        if not series_name:
            messagebox.showerror("Error", "Please select a series!", parent=self)
            return

        try:
            quantity = int(quantity_str) if quantity_str else 0
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number!", parent=self)
            return

        # Find series
        series = self.session.query(Series).filter_by(name=series_name).first()

        # Update image if selected
        if self.selected_image_path:
            with open(self.selected_image_path, "rb") as file:
                self.item.image = file.read()
            self.item.image_name = self.selected_image_path.split("/")[-1]

        # Update item
        self.item.name = name
        self.item.series = series
        self.item.quantity = quantity
        self.item.is_signature = self.is_signature_var.get()
        self.item.is_gilded = self.is_gilded_var.get()
        self.item.is_sealed = self.is_sealed_var.get()

        # Save to database
        self.session.commit()

        # Call callback
        if self.callback:
            self.callback()

        messagebox.showinfo("Success", "Item updated successfully!", parent=self)
        self.destroy()


class WishItemEditWindow(tk.Toplevel):
    def __init__(self, parent, session, wish_item, callback=None):
        super().__init__(parent)
        self.title("Edit Wish Item")
        self.geometry("500x500")

        self.session = session
        self.wish_item = wish_item
        self.callback = callback

        # Make window modal
        self.transient(parent)
        self.grab_set()

        self.setup_ui()
        self.load_item_data()

    def setup_ui(self):
        # Create input fields
        input_frame = ttk.Frame(self, padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Item Name:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.name_entry = ttk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Series:").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        self.series_combobox = ttk.Combobox(input_frame, state="readonly", width=28)
        self.series_combobox.grid(row=1, column=1, padx=5, pady=5)

        # Load series data
        series_list = self.session.query(Series).all()
        self.series_combobox["values"] = [s.name for s in series_list]

        ttk.Label(input_frame, text="Expected Price:").grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )
        self.price_entry = ttk.Entry(input_frame, width=30)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Shop URL:").grid(
            row=3, column=0, padx=5, pady=5, sticky="w"
        )
        self.url_entry = ttk.Entry(input_frame, width=30)
        self.url_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Notes:").grid(
            row=4, column=0, padx=5, pady=5, sticky="nw"
        )
        self.notes_text = tk.Text(input_frame, width=30, height=4)
        self.notes_text.grid(row=4, column=1, padx=5, pady=5)

        # Priority dropdown
        ttk.Label(input_frame, text="Priority:").grid(
            row=5, column=0, padx=5, pady=5, sticky="w"
        )
        self.priority_combobox = ttk.Combobox(
            input_frame, values=["Low", "Medium", "High"], state="readonly", width=28
        )
        self.priority_combobox.grid(row=5, column=1, padx=5, pady=5)

        # Checkbox for special features
        checkbox_frame = ttk.Frame(input_frame)
        checkbox_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        self.is_signature_var = tk.BooleanVar(value=False)
        self.is_gilded_var = tk.BooleanVar(value=False)
        self.is_sealed_var = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            checkbox_frame, text="Signature", variable=self.is_signature_var
        ).pack(side="left", padx=10)
        ttk.Checkbutton(
            checkbox_frame, text="Gilded", variable=self.is_gilded_var
        ).pack(side="left", padx=10)
        ttk.Checkbutton(
            checkbox_frame, text="Sealed", variable=self.is_sealed_var
        ).pack(side="left", padx=10)

        # Button frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Save Changes", command=self.save_changes).pack(
            side="right", padx=5
        )
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(
            side="right", padx=5
        )

    def load_item_data(self):
        # Set values from wish item
        self.name_entry.insert(0, self.wish_item.name)

        if self.wish_item.expected_price:
            self.price_entry.insert(0, self.wish_item.expected_price)

        if self.wish_item.shop_url:
            self.url_entry.insert(0, self.wish_item.shop_url)

        if self.wish_item.notes:
            self.notes_text.insert("1.0", self.wish_item.notes)

        # Set series selection
        if self.wish_item.series:
            self.series_combobox.set(self.wish_item.series.name)

        # Set priority
        self.priority_combobox.set(self.wish_item.priority)

        # Set checkbox values
        self.is_signature_var.set(bool(self.wish_item.is_signature))
        self.is_gilded_var.set(bool(self.wish_item.is_gilded))
        self.is_sealed_var.set(bool(self.wish_item.is_sealed))

    def save_changes(self):
        # Get values from form
        name = self.name_entry.get().strip()
        series_name = self.series_combobox.get()
        price = self.price_entry.get().strip()
        url = self.url_entry.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()
        priority = self.priority_combobox.get()

        # Validate
        if not name:
            messagebox.showerror("Error", "Item name is required!", parent=self)
            return

        if not series_name:
            messagebox.showerror("Error", "Please select a series!", parent=self)
            return

        # Find series
        series = self.session.query(Series).filter_by(name=series_name).first()

        # Update wish item
        self.wish_item.name = name
        self.wish_item.series = series
        self.wish_item.expected_price = price
        self.wish_item.shop_url = url
        self.wish_item.notes = notes
        self.wish_item.priority = priority
        self.wish_item.is_signature = self.is_signature_var.get()
        self.wish_item.is_gilded = self.is_gilded_var.get()
        self.wish_item.is_sealed = self.is_sealed_var.get()

        # Save to database
        self.session.commit()

        # Call callback
        if self.callback:
            self.callback()

        messagebox.showinfo(
            "Success", "Wishlist item updated successfully!", parent=self
        )
        self.destroy()


class StorageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Storage Management System")
        self.root.geometry("1000x800")

        self.session = Session()
        self.selected_image_path = None
        self.current_image = None  # Store the current PhotoImage
        self.setup_ui()

        # Load initial data
        self.refresh_series_list()
        self.refresh_list()
        self.refresh_wishlist()

    def setup_ui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Create tabs
        self.inventory_tab = ttk.Frame(self.notebook)
        self.wishlist_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.inventory_tab, text="Inventory")
        self.notebook.add(self.wishlist_tab, text="Wishlist")

        # Setup inventory tab
        self.setup_inventory_tab()

        # Setup wishlist tab
        self.setup_wishlist_tab()

    def setup_inventory_tab(self):
        # Create main frames
        self.input_frame = ttk.LabelFrame(
            self.inventory_tab, text="Add New Item", padding="10"
        )
        self.input_frame.pack(fill="x", padx=10, pady=5)

        self.list_frame = ttk.LabelFrame(
            self.inventory_tab, text="Items List", padding="10"
        )
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create preview frame
        self.preview_frame = ttk.LabelFrame(
            self.inventory_tab, text="Image Preview", padding="10"
        )
        self.preview_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Image preview label
        self.preview_label = ttk.Label(self.preview_frame)
        self.preview_label.pack(expand=True)

        # Input fields
        ttk.Label(self.input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(self.input_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Series:").grid(
            row=0, column=2, padx=5, pady=5
        )
        self.series_combobox = ttk.Combobox(self.input_frame, state="readonly")
        self.series_combobox.grid(row=0, column=3, padx=5, pady=5)

        # Series management buttons
        series_btn_frame = ttk.Frame(self.input_frame)
        series_btn_frame.grid(row=0, column=4, padx=5, pady=5)

        self.add_series_btn = ttk.Button(
            series_btn_frame, text="Add Series", command=self.open_series_window
        )
        self.add_series_btn.pack(side="left", padx=2)

        self.manage_series_btn = ttk.Button(
            series_btn_frame, text="Manage Series", command=self.open_manage_series
        )
        self.manage_series_btn.pack(side="left", padx=2)

        ttk.Label(self.input_frame, text="Quantity:").grid(
            row=1, column=0, padx=5, pady=5
        )
        self.quantity_entry = ttk.Entry(self.input_frame)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        self.image_button = ttk.Button(
            self.input_frame, text="Select Image", command=self.select_image
        )
        self.image_button.grid(row=1, column=2, padx=5, pady=5)

        self.add_button = ttk.Button(
            self.input_frame, text="Add Item", command=self.add_item
        )
        self.add_button.grid(row=1, column=3, padx=5, pady=5)

        # Checkboxes for item status
        checkbox_frame = ttk.Frame(self.input_frame)
        checkbox_frame.grid(row=2, column=0, columnspan=5, padx=5, pady=5, sticky="w")

        # Create variables for checkboxes
        self.is_signature_var = tk.BooleanVar(value=False)
        self.is_gilded_var = tk.BooleanVar(value=False)
        self.is_sealed_var = tk.BooleanVar(value=False)

        # Create checkboxes
        self.signature_check = ttk.Checkbutton(
            checkbox_frame, text="Signature", variable=self.is_signature_var
        )
        self.signature_check.pack(side="left", padx=10)

        self.gilded_check = ttk.Checkbutton(
            checkbox_frame, text="Gilded", variable=self.is_gilded_var
        )
        self.gilded_check.pack(side="left", padx=10)

        self.sealed_check = ttk.Checkbutton(
            checkbox_frame, text="Sealed", variable=self.is_sealed_var
        )
        self.sealed_check.pack(side="left", padx=10)

        # List view
        columns = (
            "id",
            "name",
            "series",
            "company",
            "quantity",
            "signature",
            "gilded",
            "sealed",
            "image_name",
        )
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show="headings")

        # Define headings
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("series", text="Series")
        self.tree.heading("company", text="Company")
        self.tree.heading("quantity", text="Quantity")
        self.tree.heading("signature", text="Signature")
        self.tree.heading("gilded", text="Gilded")
        self.tree.heading("sealed", text="Sealed")
        self.tree.heading("image_name", text="Image")

        # Column widths
        self.tree.column("id", width=50)
        self.tree.column("name", width=150)
        self.tree.column("series", width=150)
        self.tree.column("company", width=150)
        self.tree.column("quantity", width=100)
        self.tree.column("signature", width=80)
        self.tree.column("gilded", width=80)
        self.tree.column("sealed", width=80)
        self.tree.column("image_name", width=200)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            self.list_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Buttons for operations
        self.button_frame = ttk.Frame(self.list_frame)
        self.button_frame.pack(fill="x", pady=5)

        ttk.Button(
            self.button_frame, text="Delete Selected", command=self.delete_item
        ).pack(side="left", padx=5)
        ttk.Button(
            self.button_frame, text="Edit Selected", command=self.edit_item
        ).pack(side="left", padx=5)
        ttk.Button(
            self.button_frame, text="Refresh List", command=self.refresh_list
        ).pack(side="left", padx=5)
        ttk.Button(
            self.button_frame,
            text="View Series Website",
            command=self.open_series_website,
        ).pack(side="left", padx=5)
        ttk.Button(
            self.button_frame, text="View Details", command=self.show_item_details
        ).pack(side="left", padx=5)

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Bind double-click to show item details
        self.tree.bind("<Double-1>", lambda e: self.show_item_details())

    def setup_wishlist_tab(self):
        # Create frames
        wish_btn_frame = ttk.Frame(self.wishlist_tab)
        wish_btn_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(
            wish_btn_frame, text="Add Wish Item", command=self.open_wish_window
        ).pack(side="left", padx=5)
        ttk.Button(
            wish_btn_frame, text="Edit Selected", command=self.edit_wish_item
        ).pack(side="left", padx=5)
        ttk.Button(
            wish_btn_frame, text="Refresh List", command=self.refresh_wishlist
        ).pack(side="left", padx=5)
        ttk.Button(
            wish_btn_frame, text="Delete Selected", command=self.delete_wish_item
        ).pack(side="left", padx=5)
        ttk.Button(
            wish_btn_frame, text="Mark as Acquired", command=self.mark_as_acquired
        ).pack(side="left", padx=5)
        ttk.Button(wish_btn_frame, text="Open URL", command=self.open_wish_url).pack(
            side="left", padx=5
        )
        ttk.Button(
            wish_btn_frame, text="View Details", command=self.show_wish_item_details
        ).pack(side="left", padx=5)

        # Create wishlist view
        columns = (
            "id",
            "name",
            "series",
            "company",
            "price",
            "priority",
            "signature",
            "gilded",
            "sealed",
            "url",
        )
        self.wish_tree = ttk.Treeview(
            self.wishlist_tab, columns=columns, show="headings"
        )

        # Define headings
        self.wish_tree.heading("id", text="ID")
        self.wish_tree.heading("name", text="Name")
        self.wish_tree.heading("series", text="Series")
        self.wish_tree.heading("company", text="Company")
        self.wish_tree.heading("price", text="Expected Price")
        self.wish_tree.heading("priority", text="Priority")
        self.wish_tree.heading("signature", text="Signature")
        self.wish_tree.heading("gilded", text="Gilded")
        self.wish_tree.heading("sealed", text="Sealed")
        self.wish_tree.heading("url", text="Shop URL")

        # Column widths
        self.wish_tree.column("id", width=40)
        self.wish_tree.column("name", width=150)
        self.wish_tree.column("series", width=120)
        self.wish_tree.column("company", width=120)
        self.wish_tree.column("price", width=100)
        self.wish_tree.column("priority", width=80)
        self.wish_tree.column("signature", width=70)
        self.wish_tree.column("gilded", width=70)
        self.wish_tree.column("sealed", width=70)
        self.wish_tree.column("url", width=150)

        # Add scrollbar
        wish_scrollbar = ttk.Scrollbar(
            self.wishlist_tab, orient="vertical", command=self.wish_tree.yview
        )
        self.wish_tree.configure(yscrollcommand=wish_scrollbar.set)
        wish_scrollbar.pack(side="right", fill="y")
        self.wish_tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Notes frame
        notes_frame = ttk.LabelFrame(self.wishlist_tab, text="Notes", padding="10")
        notes_frame.pack(fill="x", padx=10, pady=10)

        self.wish_notes_text = tk.Text(notes_frame, height=5, wrap="word")
        self.wish_notes_text.pack(fill="both", expand=True)
        self.wish_notes_text.config(state="disabled")

        # Bind selection event
        self.wish_tree.bind("<<TreeviewSelect>>", self.on_wish_select)

        # Bind double-click to show item details
        self.wish_tree.bind("<Double-1>", lambda e: self.show_wish_item_details())

    def open_wish_window(self):
        WishItemWindow(self.root, self.session, callback=self.refresh_wishlist)

    def on_wish_select(self, event):
        selected_items = self.wish_tree.selection()
        if not selected_items:
            self.wish_notes_text.config(state="normal")
            self.wish_notes_text.delete("1.0", tk.END)
            self.wish_notes_text.config(state="disabled")
            return

        wish_id = self.wish_tree.item(selected_items[0])["values"][0]
        wish_item = self.session.query(WishItem).get(wish_id)

        if wish_item and wish_item.notes:
            self.wish_notes_text.config(state="normal")
            self.wish_notes_text.delete("1.0", tk.END)
            self.wish_notes_text.insert("1.0", wish_item.notes)
            self.wish_notes_text.config(state="disabled")
        else:
            self.wish_notes_text.config(state="normal")
            self.wish_notes_text.delete("1.0", tk.END)
            self.wish_notes_text.insert("1.0", "No notes available.")
            self.wish_notes_text.config(state="disabled")

    def refresh_wishlist(self):
        # Clear existing items
        for item in self.wish_tree.get_children():
            self.wish_tree.delete(item)

        # Load wishlist items from database
        wish_items = self.session.query(WishItem).all()
        for item in wish_items:
            self.wish_tree.insert(
                "",
                "end",
                values=(
                    item.id,
                    item.name,
                    item.series.name if item.series else "",
                    item.series.company_name if item.series else "",
                    item.expected_price if item.expected_price else "-",
                    item.priority,
                    "Yes" if getattr(item, "is_signature", False) else "No",
                    "Yes" if getattr(item, "is_gilded", False) else "No",
                    "Yes" if getattr(item, "is_sealed", False) else "No",
                    item.shop_url or "-",
                ),
            )

    def delete_wish_item(self):
        selected = self.wish_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to delete!")
            return

        if messagebox.askyesno(
            "Confirm", "Are you sure you want to delete this wishlist item?"
        ):
            wish_id = self.wish_tree.item(selected[0])["values"][0]
            wish_item = self.session.query(WishItem).get(wish_id)
            self.session.delete(wish_item)
            self.session.commit()
            self.refresh_wishlist()

    def mark_as_acquired(self):
        selected = self.wish_tree.selection()
        if not selected:
            messagebox.showwarning(
                "Warning", "Please select an item to mark as acquired!"
            )
            return

        wish_id = self.wish_tree.item(selected[0])["values"][0]
        wish_item = self.session.query(WishItem).get(wish_id)

        # Ask for quantity
        quantity = simpledialog.askinteger(
            "Quantity", "Enter quantity acquired:", minvalue=1, initialvalue=1
        )
        if not quantity:  # User canceled
            return

        # Create a new inventory item
        new_item = Item(
            name=wish_item.name,
            series=wish_item.series,
            quantity=quantity,
            is_signature=wish_item.is_signature,
            is_gilded=wish_item.is_gilded,
            is_sealed=wish_item.is_sealed,
        )

        self.session.add(new_item)

        # Delete from wishlist
        if messagebox.askyesno(
            "Remove from Wishlist", "Remove this item from your wishlist?"
        ):
            self.session.delete(wish_item)

        self.session.commit()

        # Refresh both lists
        self.refresh_wishlist()
        self.refresh_list()
        messagebox.showinfo(
            "Success", "Item marked as acquired and added to inventory!"
        )

    def open_series_window(self):
        SeriesWindow(self.root, self.session, callback=self.refresh_series_list)

    def open_manage_series(self):
        SeriesManageWindow(
            self.root, self.session, refresh_callback=self.refresh_series_list
        )

    def refresh_series_list(self):
        series_list = self.session.query(Series).all()
        self.series_combobox["values"] = [s.name for s in series_list]
        if series_list:
            self.series_combobox.set(series_list[0].name)
        self.refresh_list()  # Also refresh items list in case series were deleted

    def select_image(self):
        self.selected_image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if self.selected_image_path:
            self.image_button.configure(text="Image Selected")
            self.show_preview(self.selected_image_path)

    def show_preview(self, image_path=None, image_data=None):
        try:
            if image_path:
                image = Image.open(image_path)
            elif image_data:
                image = Image.open(io.BytesIO(image_data))
            else:
                self.preview_label.configure(image="")
                return

            # Resize image to fit preview (max 300x300)
            image.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(image)
            self.current_image = photo  # Keep a reference!
            self.preview_label.configure(image=photo)
        except Exception as e:
            print(f"Error showing preview: {e}")
            self.preview_label.configure(image="")

    def on_select(self, event):
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item_id = self.tree.item(selected_items[0])["values"][0]
        item = self.session.query(Item).get(item_id)

        if item and item.image:
            self.show_preview(image_data=item.image)
        else:
            self.preview_label.configure(image="")

    def add_item(self):
        name = self.name_entry.get().strip()
        series_name = self.series_combobox.get()
        quantity = self.quantity_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Name is required!")
            return

        if not series_name:
            messagebox.showerror("Error", "Please select or add a series!")
            return

        try:
            quantity = int(quantity) if quantity else 0
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number!")
            return

        series = self.session.query(Series).filter_by(name=series_name).first()

        image_data = None
        image_name = None
        if self.selected_image_path:
            with open(self.selected_image_path, "rb") as file:
                image_data = file.read()
            image_name = self.selected_image_path.split("/")[-1]

        # Get checkbox values
        is_signature = self.is_signature_var.get()
        is_gilded = self.is_gilded_var.get()
        is_sealed = self.is_sealed_var.get()

        new_item = Item(
            name=name,
            series=series,
            quantity=quantity,
            image=image_data,
            image_name=image_name,
            is_signature=is_signature,
            is_gilded=is_gilded,
            is_sealed=is_sealed,
        )

        self.session.add(new_item)
        self.session.commit()

        self.clear_inputs()
        self.refresh_list()
        messagebox.showinfo("Success", "Item added successfully!")

    def clear_inputs(self):
        self.name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.selected_image_path = None
        self.image_button.configure(text="Select Image")
        self.preview_label.configure(image="")

        # Reset checkboxes
        self.is_signature_var.set(False)
        self.is_gilded_var.set(False)
        self.is_sealed_var.set(False)

    def delete_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to delete!")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this item?"):
            item_id = self.tree.item(selected_item)["values"][0]
            item = self.session.query(Item).get(item_id)
            self.session.delete(item)
            self.session.commit()
            self.refresh_list()
            self.preview_label.configure(image="")

    def refresh_list(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load items from database
        items = self.session.query(Item).all()
        for item in items:
            self.tree.insert(
                "",
                "end",
                values=(
                    item.id,
                    item.name,
                    item.series.name if item.series else "",
                    item.series.company_name if item.series else "",
                    item.quantity,
                    "Yes" if getattr(item, "is_signature", False) else "No",
                    "Yes" if getattr(item, "is_gilded", False) else "No",
                    "Yes" if getattr(item, "is_sealed", False) else "No",
                    item.image_name or "No image",
                ),
            )

    def open_series_website(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item first!")
            return

        item_id = self.tree.item(selected[0])["values"][0]
        item = self.session.query(Item).get(item_id)

        if item and item.series and item.series.shop_website:
            url = item.series.shop_website
            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            webbrowser.open(url)
        else:
            messagebox.showinfo("Info", "No website available for this item's series.")

    def open_wish_url(self):
        selected = self.wish_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to view URL!")
            return

        wish_id = self.wish_tree.item(selected[0])["values"][0]
        wish_item = self.session.query(WishItem).get(wish_id)

        if wish_item and wish_item.shop_url:
            url = wish_item.shop_url
            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            webbrowser.open(url)
        else:
            messagebox.showinfo("Info", "No URL available for this item.")

    def show_item_details(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item first!")
            return

        item_id = self.tree.item(selected[0])["values"][0]
        item = self.session.query(Item).get(item_id)

        if item:
            ItemDetailsWindow(self.root, item, "inventory")
        else:
            messagebox.showerror("Error", "Item not found!")

    def show_wish_item_details(self):
        selected = self.wish_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item first!")
            return

        wish_id = self.wish_tree.item(selected[0])["values"][0]
        wish_item = self.session.query(WishItem).get(wish_id)

        if wish_item:
            ItemDetailsWindow(self.root, wish_item, "wishlist")
        else:
            messagebox.showerror("Error", "Item not found!")

    def edit_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to edit!")
            return

        item_id = self.tree.item(selected[0])["values"][0]
        item = self.session.query(Item).get(item_id)

        if item:
            ItemEditWindow(self.root, self.session, item, callback=self.refresh_list)
        else:
            messagebox.showerror("Error", "Item not found!")

    def edit_wish_item(self):
        selected = self.wish_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to edit!")
            return

        wish_id = self.wish_tree.item(selected[0])["values"][0]
        wish_item = self.session.query(WishItem).get(wish_id)

        if wish_item:
            WishItemEditWindow(
                self.root, self.session, wish_item, callback=self.refresh_wishlist
            )
        else:
            messagebox.showerror("Error", "Item not found!")


if __name__ == "__main__":
    root = tk.Tk()
    app = StorageApp(root)
    root.mainloop()
