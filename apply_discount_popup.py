import tkinter as tk
from tkinter import messagebox
import requests
import re

class ApplyDiscountPopup(tk.Frame):
    """ Popup Frame to apply discount """

    def __init__(self, parent, selected_product, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)
        
        tk.Label(self, text="Discount:").grid(row=2, column=1)
        self._discount = tk.DoubleVar()  
        self._discount_entry = tk.Entry(self, textvariable=self._discount)
        self._discount_entry.grid(row=2, column=2)

        tk.Button(self, text="Submit", command=self._submit_cb).grid(row=7, column=1)
        tk.Button(self, text="Close", command=self._close_cb).grid(row=7, column=2)

        if selected_product is not None:
            self._selected_id = selected_product["id"]
            self._discount_entry.insert(0, str(selected_product.get("discount", 0)))
           
        else:
            self._selected_id = None

    def _submit_cb(self):
        """ Submit Complete Repair """

        discount = self._discount_entry.get()

        if discount is None or re.match(r"^\d+(\.\d{1,2})+$", str(discount)) is None:
            messagebox.showerror("Validation Error", "Discount is invalid")
            return
        try:
            discount = float(discount)
        except ValueError:
            messagebox.showerror("Validation Error", "Enter valid discount.")
            return

        if self._selected_id is not None:
            self._apply_discount(self._selected_id, discount)
        
    def _apply_discount(self, product_id, discount):
        """ Applies discount to the product """

        data = {
            'discount': discount
        }

        print(product_id)

        headers = {"content-type": "application/json"}

        try:
            response = requests.put(f"http://127.0.0.1:5001/productshop/products/discount/{product_id}", json=data, headers=headers)
            response.raise_for_status()
            self._close_cb()
        except requests.exceptions.HTTPError as err:
            messagebox.showerror("Error", f"Update Makeup Product Failed: {err}")
        except Exception as err:
            messagebox.showerror("Error", f"An unexpected error occurred: {err}")
        if response is not None and response.status_code == 200:
            self._close_cb()
        else:
            messagebox.showerror("Error", "Failed to apply discount: " + response.text)
        