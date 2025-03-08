import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import io
from models import Session, Item, Series


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


class StorageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Storage Management System")
        self.root.geometry("1000x800")

        self.session = Session()
        self.selected_image_path = None
        self.current_image = None  # Store the current PhotoImage
        self.setup_ui()

    def setup_ui(self):
        # Create main frames
        self.input_frame = ttk.LabelFrame(self.root, text="Add New Item", padding="10")
        self.input_frame.pack(fill="x", padx=10, pady=5)

        self.list_frame = ttk.LabelFrame(self.root, text="Items List", padding="10")
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create preview frame
        self.preview_frame = ttk.LabelFrame(
            self.root, text="Image Preview", padding="10"
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

        # Add Series button
        self.add_series_btn = ttk.Button(
            self.input_frame, text="Add New Series", command=self.open_series_window
        )
        self.add_series_btn.grid(row=0, column=4, padx=5, pady=5)

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

        # List view
        columns = ("id", "name", "series", "company", "quantity", "image_name")
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show="headings")

        # Define headings
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("series", text="Series")
        self.tree.heading("company", text="Company")
        self.tree.heading("quantity", text="Quantity")
        self.tree.heading("image_name", text="Image")

        # Column widths
        self.tree.column("id", width=50)
        self.tree.column("name", width=150)
        self.tree.column("series", width=150)
        self.tree.column("company", width=150)
        self.tree.column("quantity", width=100)
        self.tree.column("image_name", width=200)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            self.list_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Buttons for operations
        self.button_frame = ttk.Frame(self.list_frame)
        self.button_frame.pack(fill="x", pady=5)

        ttk.Button(
            self.button_frame, text="Delete Selected", command=self.delete_item
        ).pack(side="left", padx=5)
        ttk.Button(
            self.button_frame, text="Refresh List", command=self.refresh_list
        ).pack(side="left", padx=5)

        # Load initial data
        self.refresh_series_list()
        self.refresh_list()

    def open_series_window(self):
        SeriesWindow(self.root, self.session, callback=self.refresh_series_list)

    def refresh_series_list(self):
        series_list = self.session.query(Series).all()
        self.series_combobox["values"] = [s.name for s in series_list]
        if series_list:
            self.series_combobox.set(series_list[0].name)

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

        new_item = Item(
            name=name,
            series=series,
            quantity=quantity,
            image=image_data,
            image_name=image_name,
        )

        self.session.add(new_item)
        self.session.commit()

        self.clear_inputs()
        self.refresh_list()
        messagebox.showinfo("Success", "Item added successfully!")

    def clear_inputs(self):
        self.name_entry.delete(0, tk.END)
        self.series_combobox.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.selected_image_path = None
        self.image_button.configure(text="Select Image")
        self.preview_label.configure(image="")

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
                    item.image_name or "No image",
                ),
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = StorageApp(root)
    root.mainloop()
