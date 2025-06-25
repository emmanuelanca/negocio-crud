import tkinter as tk
from tkinter import ttk
import psycopg2
from tksheet import Sheet

# Database connection parameters
DB_NAME = "DbEmmanuel"
DB_USER = "emmanuel"
DB_PASSWORD = "adsf"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_SCHEMA = "negocio"

def fetch_data(table_name):
    """Fetch all rows from specified table under negocio schema."""
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {DB_SCHEMA}.{table_name} LIMIT 100;")  # limit for demo
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        cur.close()
        return columns, rows
    except Exception as e:
        print(f"Error fetching data from {table_name}: {e}")
        return [], []
    finally:
        if conn:
            conn.close()

def create_tab(tab_frame, table_name):
    """Create a sheet that fills the available space horizontally and vertically."""
    # Outer container fills the entire tab
    outer = ttk.Frame(tab_frame)
    outer.pack(expand=True, fill="both")

    # Configure the grid to expand
    outer.columnconfigure(0, weight=1)
    outer.rowconfigure(0, weight=1)

    columns, rows = fetch_data(table_name)

    # Sheet directly inside outer frame
    sheet = Sheet(
        outer,
        headers=columns,
        show_row_index=False,
        editable=True
    )
    sheet.enable_bindings((
        "single_select",
        "edit_cell",
        "arrowkeys",
        "undo",
        "redo"
    ))
    sheet.grid(row=0, column=0, sticky="nsew")  # fill in all directions

    sheet.set_sheet_data(rows)
    return sheet

            
def main():
    root = tk.Tk()
    root.title("Gestor de negocio")
    root.geometry("900x500")

    tab_control = ttk.Notebook(root)

    # Tab Productos
    tab_productos = ttk.Frame(tab_control)
    tab_control.add(tab_productos, text="Productos")

    # Tab Proveedores
    tab_proveedores = ttk.Frame(tab_control)
    tab_control.add(tab_proveedores, text="Proveedores")

    tab_control.pack(expand=1, fill="both")

    # Create sheets in tabs
    create_tab(tab_productos, "producto")
    create_tab(tab_proveedores, "proveedor")

    root.mainloop()

if __name__ == "__main__":
    main()
