import tkinter as tk
import requests
from add_makeup_popup import AddUpdateMakeupPopup
from add_skincare_popup import AddUpdateSkincarePopup
from apply_discount_popup import ApplyDiscountPopup
from repair_stats import RepairStats
from skincare_product import SkinCare
from makeup_product import MakeUp
from tkinter import messagebox
from details import DetailsPopup

class MainAppController(tk.Frame):
    """ Main Application for GUI """
    
    def __init__(self, parent):
        """ Initialize Main Application """

        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Products List").grid(row=1, column=1)
        
        self._makeup_listbox = tk.Listbox(self)
        self._makeup_listbox.grid(row=2, column=0, columnspan=7)

        self._skincare_listbox = tk.Listbox(self)
        self._skincare_listbox.grid(row=2, column=0, columnspan=7)
        
        self._products = []
        self._entity_type = tk.IntVar(value=1)

        tk.Radiobutton(self, text="Makeup", variable=self._entity_type, value=1, command=self._show_makeup_listbox).grid(row=2, column=0)
        tk.Radiobutton(self, text="Skincare", variable=self._entity_type, value=2, command=self._show_skincare_listbox).grid(row=3, column=0)

        tk.Button(self, text="Add Makeup Product", command=self._add_makeup_product).grid(row=4, column=1)
        tk.Button(self, text="Add Skincare Product", command=self._add_skincare_product).grid(row=4, column=2)
        tk.Button(self, text="Update Makeup Product", command=self._update_makeup_product).grid(row=4, column=3)
        tk.Button(self, text="Update Skincare Product", command=self._update_skincare_product).grid(row=4, column=4)
        tk.Button(self, text="Display Full Details", command=self._display_full_details).grid(row=4, column=5)
        tk.Button(self, text="Remove Makeup Product", command=self._remove_makeup_product).grid(row=5, column=3)
        tk.Button(self, text="Remove Skincare Product", command=self._remove_skincare_product).grid(row=5, column=4)
        tk.Button(self, text="Apply Discount", command=self._apply_discount).grid(row=5, column=5)
        tk.Button(self, text="Quit", command=self._quit_callback).grid(row=5, column=6)

        self._total_discount = tk.Label(self, text="Total Discount: ")
        self._total_discount.grid(row=6, column=3, sticky=tk.E)

        self._num_makeup_products = tk.Label(self, text="Number of Makeup Products: ")
        self._num_makeup_products.grid(row=7, column=3, sticky=tk.E)

        self._num_skincare_products = tk.Label(self, text="Number of Skincare Products: ")
        self._num_skincare_products.grid(row=8, column=3, sticky=tk.E)

        self._num_discounted_products= tk.Label(self, text="Number of Discounted Products: ")
        self._num_discounted_products.grid(row=9, column=3, sticky=tk.E)

        self._num_non_discounted_products = tk.Label(self, text="Number of non-discounted Products: ")
        self._num_non_discounted_products.grid(row=10, column=3, sticky=tk.E)

        self._update_products_list()
        self._calculate_stats()  

    def _show_makeup_listbox(self):
        """ Shows the Makeup Listbox"""

        self._skincare_listbox.grid_forget()  
        self._makeup_listbox.grid(row=2, column=1, columnspan=7)  
        self._update_products_list()
        # self._calculate_stats()


    def _show_skincare_listbox(self):
        """ Shows the Skincare Listbox"""

        self._makeup_listbox.grid_forget()  
        self._skincare_listbox.grid(row=2, column=1, columnspan=7)  
        self._update_products_list()
        # self._calculate_stats()

    def _close_cb(self):
        """ Close Update product popup """
        self._popup_win.destroy()
        self._update_products_list()
        self._calculate_stats()

    def _add_makeup_product(self):
        """ Add Makeup Product Popup """

        self._popup_win = tk.Toplevel()
        self._popup = AddUpdateMakeupPopup(self._popup_win, None, self._close_cb)
        # self._calculate_stats()

    def _add_skincare_product(self):
        """ Add Skincare Product Popup """

        self._popup_win = tk.Toplevel()
        self._popup = AddUpdateSkincarePopup(self._popup_win, None, self._close_cb)
        # self._calculate_stats()

    def _update_makeup_product(self):
        """ Update Makeup Product popup """
        
        selection = self._makeup_listbox.curselection() 
        if selection is None or len(selection) == 0:
            messagebox.showwarning("Warning", "No Makeup product selected to update. Click on Makeup Button on the left and Select from Makeup Products List")
            return 

        index = selection[0]
        if self._entity_type.get() == 1:
            products_list = self._makeup_products
        elif self._entity_type.get() == 2:
            products_list = self._skincare_products
        
        else:
            messagebox.showinfo("Error", "Invalid entity type.")
            return

        if index < 0 or index >= len(products_list):  
            messagebox.showinfo("Error", "Invalid product index.")
            return

        product = products_list[index]

        self._popup_win = tk.Toplevel()
        self._popup = AddUpdateMakeupPopup(self._popup_win, product, self._close_cb)

        # self._calculate_stats()

    def _update_skincare_product(self):
        """ Update Skincare Product popup """

        selection = self._skincare_listbox.curselection() 
        if selection is None or len(selection) == 0:
            messagebox.showwarning("Warning", "No Skincare product selected to update. Click on Skincare Button on the left and Select from Skincare Products List")
            return 

        index = selection[0]
        if self._entity_type.get() == 1:
            products_list = self._makeup_products
        elif self._entity_type.get() == 2:
            products_list = self._skincare_products
        else:
            messagebox.showinfo("Error", "Invalid entity type.")
            return

        if index < 0 or index >= len(products_list):  
            messagebox.showinfo("Error", "Invalid product index.")
            return

        product = products_list[index]

        self._popup_win = tk.Toplevel()
        self._popup = AddUpdateSkincarePopup(self._popup_win, product, self._close_cb)

        # self._calculate_stats()


    def _update_products_list(self):
        """ Updates the Makeup and Skincare Prodcut List"""

        headers = {"content-type": "application/json"}

        try:
            response_makeup_descs = requests.get(f"http://127.0.0.1:5001/productshop/products/all/{MakeUp.TYPE}", headers=headers)
            response_makeup_descs.raise_for_status()
            makeup_descs = response_makeup_descs.json()
        except requests.exceptions.RequestException as err:
            messagebox.showerror("Error", f"Error fetching makeup products: {err}")
            makeup_descs = []

        try:
            response_skincare_descs = requests.get(f"http://127.0.0.1:5001/productshop/products/all/{SkinCare.TYPE}", headers=headers)
            response_skincare_descs.raise_for_status()
            skincare_descs = response_skincare_descs.json()
        except requests.exceptions.RequestException as err:
            messagebox.showerror("Error", f"Error fetching skincare products: {err}")
            skincare_descs = []

       
        if self._entity_type.get() == 1:
            self._makeup_products = makeup_descs
        else:
            self._makeup_products = []

        if self._entity_type.get() == 2:
            self._skincare_products = skincare_descs
        else:
            self._skincare_products = []

        if self._entity_type.get() == 1:
            self._makeup_listbox.delete(0, tk.END)
            for makeup_desc in self._makeup_products:
                product_summary = f"{makeup_desc['brand']} {makeup_desc['name']} in {makeup_desc['shade']} "
                self._makeup_listbox.insert(tk.END, product_summary)
        else:
            self._makeup_listbox.grid_forget()

        if self._entity_type.get() == 2:
            self._skincare_listbox.delete(0, tk.END)
            for skincare_desc in self._skincare_products:
                product_summary = f"{skincare_desc['brand']} {skincare_desc['name']} for {skincare_desc['skin_type']} skin "

                self._skincare_listbox.insert(tk.END, product_summary)
        else:
            self._skincare_listbox.grid_forget()

        # self._calculate_stats()
    
    def _remove_makeup_product(self):
        """ Remove Makeup Product """

        selection = self._makeup_listbox.curselection()
        if selection is None or len(selection) == 0:
            messagebox.showwarning("Warning", "No Makeup product selected to delete. Click on Makeup Button on the left and Select from Makeup Products List")
            return 

        index = selection[0]
        if self._entity_type.get() == 1:
            products_list = self._makeup_products
        elif self._entity_type.get() == 2:
            products_list = self._skincare_products
        else:
            messagebox.showinfo("Error", "Invalid entity type.")
            return

        if index < 0 or index >= len(products_list): 
            messagebox.showinfo("Error", "Invalid product index.")
            return

        product = products_list[index]
        result = messagebox.askyesno("Confirm", "Are you sure you want to delete the product?")
       
        if result:
            requests.delete("http://127.0.0.1:5001/productshop/products/" + str(product["id"]))
            self._update_products_list()

        self._calculate_stats()

    def _remove_skincare_product(self):
        """ Remove Skincare Product """

        selection = self._skincare_listbox.curselection()
        if selection is None or len(selection) == 0:
            messagebox.showwarning("Warning", "No Skincare product selected to delete. Click on Skincare Button on the left and Select from Skincare Products List")
            return 

        index = selection[0]
        if self._entity_type.get() == 1:
            products_list = self._makeup_products
        elif self._entity_type.get() == 2:
            products_list = self._skincare_products
        else:
            messagebox.showinfo("Error", "Invalid entity type.")
            return

        if index < 0 or index >= len(products_list): 
            messagebox.showinfo("Error", "Invalid product index.")
            return

        product = products_list[index]
        result = messagebox.askyesno("Confirm", "Are you sure you want to delete the product?")
       
        if result:
            requests.delete("http://127.0.0.1:5001/productshop/products/" + str(product["id"]))
            self._update_products_list()

        self._calculate_stats()

    def _quit_callback(self):
        """ Quit """

        self.quit()

    def _display_full_details(self):
        """ Details Popup"""

        selection = None
        if self._entity_type.get() == 1:
            selection = self._makeup_listbox.curselection()
        elif self._entity_type.get() == 2:
            selection = self._skincare_listbox.curselection()

        if selection is None or len(selection) == 0:
            messagebox.showwarning("Warning", "No product selected to view. Click on Button on the left and Select from Makeup or Skincare Products List")
            return

        index = selection[0]

        if self._entity_type.get() == 1:
            products_list = self._makeup_products
        elif self._entity_type.get() == 2:
            products_list = self._skincare_products

        if index < 0 or index >= len(products_list):  
            messagebox.showinfo("Error", "Invalid product index.")
            return

        product = products_list[index]
        self._popup_win = tk.Toplevel()
        self._popup_win.title("Product Details")

        self._popup = DetailsPopup(self._popup_win, product, self._close_cb)
        # self._calculate_stats()

    def _apply_discount(self):
        """ Apply Discount Popup """

        selection = None
        if self._entity_type.get() == 1:
            selection = self._makeup_listbox.curselection()
        elif self._entity_type.get() == 2:
            selection = self._skincare_listbox.curselection()

        if selection is None or len(selection) == 0:
            messagebox.showwarning("Warning", "No product selected. Click on Button on the left and Select from Makeup or Skincare Products List")
            return

        index = selection[0]

        if self._entity_type.get() == 1:
            products_list = self._makeup_products
        elif self._entity_type.get() == 2:
            products_list = self._skincare_products

        if index < 0 or index >= len(products_list):  
            messagebox.showinfo("Error", "Invalid product index.")
            return

        product = products_list[index]
        self._popup_win = tk.Toplevel()
        self._popup_win.title("Product Discount")

        self._popup = ApplyDiscountPopup(self._popup_win, product, self._close_cb)
        # self._calculate_stats()
        

    def _calculate_stats(self):
        """ Calculate discount statistics and update labels """

        headers = {"content-type": "application/json"}

        response_stats = requests.get("http://127.0.0.1:5001/productshop/repairstats", headers=headers)

        if response_stats.status_code != 200:
            messagebox.showerror("Error", f"Error fetching repair stats: {response_stats.status_code}")
            return

        stats = response_stats.json()

        total_discounted_price = stats.get('total_discounted_price', 0.0)
        num_makeup_products = stats.get('num_makeup_products', 0)
        num_skincare_products = stats.get('num_skincare_products', 0)
        num_discounted_products = stats.get('num_discounted_products', 0)
        num_non_discounted_products = stats.get('num_non_discounted_products',0)

        RepairStats(int(num_makeup_products), int(num_skincare_products), int(num_discounted_products), int(num_non_discounted_products),float(total_discounted_price))

        self._num_makeup_products.config(text="Number of Makeup Products: " + str(num_makeup_products))
        self._num_skincare_products.config(text="Number of Skincare Products: " + str(num_skincare_products))
        self._num_discounted_products.config(text="Number of Discounted Products: " + str(num_discounted_products))
        self._num_non_discounted_products.config(text="Number of Non-Discounted Products: " + str(num_non_discounted_products))
        self._total_discount.config(text="Total Discounted Price: " + str(total_discounted_price))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Beauty Product Discounts")
    root.geometry("1100x400")
    MainAppController(root).pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    root.mainloop()
