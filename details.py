import tkinter as tk
from tkinter import messagebox
import requests

class DetailsPopup(tk.Frame):
    """ Popup Frame to get details """

    def __init__(self, parent, selected_product, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        tk.Label(self, text="Detail:").grid(row=1, column=1)
        if selected_product is not None:
            self._selected_id = selected_product["id"]
        else:
            self._selected_id = None

        if self._selected_id is not None:
            self._display_product(self._selected_id)

    def _display_product(self, product_id):
        """ displays the product """

        headers = {"content-type": "application/json"}

        try:
            response = requests.get(f"http://127.0.0.1:5001/productshop/products/details/{product_id}", headers=headers)
            response.raise_for_status()
            product_details = response.json()
            tk.Label(self, text=product_details, justify=tk.LEFT).grid(row=2, column=1)
        except requests.exceptions.RequestException as err:
            messagebox.showerror("Error", f"Error fetching product details: {err}")
        except ValueError as err:
            messagebox.showerror("Error", f"Error parsing product details: {err}")

        tk.Button(self, text="Close", command=self._close_cb).grid(row=4, column=2)
