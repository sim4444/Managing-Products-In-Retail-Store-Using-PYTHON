import tkinter as tk
from tkinter import messagebox
import requests
import re

class AddUpdateMakeupPopup(tk.Frame):
    """ Popup Frame to Add a Phone """

    def __init__(self, parent, selected_product, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        tk.Label(self, text="Name:").grid(row=2, column=1)
        self._name_entry = tk.Entry(self)
        self._name_entry.grid(row=2, column=2)

        tk.Label(self, text="Brand:").grid(row=3, column=1)
    
        self._brand_entry = tk.Entry(self)
        self._brand_entry.grid(row=3, column=2)

        tk.Label(self, text="Packaging:").grid(row=4, column=1)
          
        self._packaging_entry = tk.Entry(self)
        self._packaging_entry.grid(row=4, column=2)

        tk.Label(self, text="Price:").grid(row=5, column=1)
        self._price_entry = tk.Entry(self)
        self._price_entry.grid(row=5, column=2)

        tk.Label(self, text="Rating:").grid(row=6, column=1)
        self._rating_entry = tk.Entry(self)
        self._rating_entry.grid(row=6, column=2)

        tk.Label(self, text="Shade:").grid(row=7, column=1)
        self._shade_entry = tk.Entry(self)
        self._shade_entry.grid(row=7, column=2)
        
        tk.Label(self, text="Waterproof:").grid(row=9, column=1)
        self._waterproof = tk.BooleanVar()
        self._waterproof_entry = tk.Checkbutton(self, variable=self._waterproof)
        self._waterproof_entry.grid(row=9, column=2)

        tk.Button(self, text="Submit", command=self._submit_cb).grid(row=11, column=1)
        tk.Button(self, text="Close", command=self._close_cb).grid(row=11, column=2)

        if selected_product is not None:
            self._selected_id = selected_product["id"]
            self._name_entry.insert(0, (selected_product["name"]))
            self._brand_entry.insert(0, (selected_product["brand"]))
            self._packaging_entry.insert(0, (selected_product["packaging"]))
            self._price_entry.insert(0, (selected_product["price"]))
            self._rating_entry.insert(0, (selected_product["rating"]))
            self._shade_entry.insert(0, (selected_product["shade"]))
        else:
            self._selected_id = None


    def _submit_cb(self):
        """ Submit the Add Phone """

        if self._name_entry.get() is None or re.match(r"^[A-Za-z0-9\-]+$", self._name_entry.get()) is None:
            messagebox.showerror("Validation Error", "Name is invalid")
            return
        
        if self._brand_entry.get() is None or re.match(r"^[A-Za-z0-9\-]+$", self._brand_entry.get()) is None:
            messagebox.showerror("Validation Error", "Brand is invalid")
            return
        
        if self._packaging_entry.get() is None or re.match(r"^[A-Za-z0-9\-]+$",(self._packaging_entry.get())) is None:
            messagebox.showerror("Validation Error", "Packaging is invalid")
            return
        
        if self._price_entry.get() is None or re.match(r"^\d+.\d{2}$", str(self._price_entry.get())) is None:

            messagebox.showerror("Validation Error", "Price is invalid")
            return
        
        if self._rating_entry.get() is None or re.match(r"^\d+.\d{2}$", str(self._rating_entry.get())) is None:
            messagebox.showerror("Validation Error", "Rating is invalid")
            return
        
        
        if self._shade_entry.get() is None or re.match(r"^[A-Za-z0-9\-]+$", (self._shade_entry.get())) is None:
            messagebox.showerror("Validation Error", "Shade is invalid")
            return

        
        data = {}
        data['name'] = self._name_entry.get()
        data['brand'] = self._brand_entry.get()
        data['packaging'] = self._packaging_entry.get()
        data['rating'] = float(self._rating_entry.get())
        data['price'] = float(self._price_entry.get())       
        data['shade'] = self._shade_entry.get()
        data['waterproof'] = self._waterproof.get()
        data['type'] = "Makeup" 
        
        if self._selected_id is None:
            self._add_makeup_product(data)
        else:
            self._update_makeup_product(self._selected_id, data)

    def _add_makeup_product(self, data):
        """ Adds the makeup product """

        headers = {"content-type": "application/json"}

        try:
            response = requests.post("http://127.0.0.1:5001/productshop/products", json=data, headers=headers)
            response.raise_for_status()  
            self._close_cb()
        except requests.exceptions.HTTPError as err:
            messagebox.showerror("Error", f"Add Makeup Product Failed: {err}")
        except Exception as err:
            messagebox.showerror("Error", f"An unexpected error occurred: {err}")

    def _update_makeup_product(self, product_id, data):
        """ Updates the makeup product """

        print(product_id)

        headers = {"content-type": "application/json"}

        try:
            response = requests.put("http://127.0.0.1:5001/productshop/products/" + str(product_id), json=data, headers=headers)
            response.raise_for_status()
            self._close_cb()
        except requests.exceptions.HTTPError as err:
            messagebox.showerror("Error", f"Update Makeup Product Failed: {err}")
        except Exception as err:
            messagebox.showerror("Error", f"An unexpected error occurred: {err}")
        if response.status_code == 200:
            self._close_cb()
        else:
            messagebox.showerror("Error", "Cannot update Product because: " + response.text)


        