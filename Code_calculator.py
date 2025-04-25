import tkinter as tk
from tkinter import ttk, messagebox


def formato(valor):
    return f"${valor:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")

def formatear_valor_producto(event):
    entry = event.widget
    valor = entry.get().replace(".", "").strip()

    if valor.isdigit():
        numero = int(valor)
        entry.delete(0, tk.END)
        entry.insert(0, f"{numero:,}".replace(",", "."))
    elif valor == "":
        entry.delete(0, tk.END)

def calcular_descuento():
    try:
        base = float(entry_base.get().replace(".", ""))
        comision1 = float(entry_comision1.get().replace(",", "."))
        comision2 = float(entry_comision2.get().replace(",", "."))

        if base < 0 or comision1 < 0 or comision2 < 0:
            raise ValueError("Los valores deben ser positivos.")

        factor_iva = 1.19 if var_iva_activado.get() else 1

        desc1_base = base * (comision1 / 100)
        desc1_total = desc1_base * factor_iva

        desc2_base = base * (comision2 / 100)
        desc2_total = desc2_base * factor_iva

        descuento_total = desc1_total + desc2_total
        resultado_final = base - descuento_total

        mostrar_resultado(formato(resultado_final))
        detalle_label.config(text=(
            f"「Comisión por venta」 ➔ Descuento: -{formato(desc1_total)}\n"
            f"「Anticipo de abono」 ➔ Descuento: -{formato(desc2_total)}\n"
            f"--------------------------------------------\n"
            f"「Total descontado」: -{formato(descuento_total)}"
        ), foreground="#cc0000")

    except ValueError as e:
        mostrar_resultado("✘ ERROR ✘")
        detalle_label.config(text="", foreground="white")
        messagebox.showerror("✘ Error de ingreso ✘", str(e))

def mostrar_resultado(valor):
    pantalla_resultado.config(state='normal')
    pantalla_resultado.delete(0, tk.END)
    pantalla_resultado.insert(0, valor)
    pantalla_resultado.config(state='readonly')

def limpiar_campos():
    entry_base.delete(0, tk.END)
    entry_comision1.delete(0, tk.END)
    entry_comision2.delete(0, tk.END)
    var_iva_activado.set(True)
    pantalla_resultado.config(state='normal')
    pantalla_resultado.delete(0, tk.END)
    pantalla_resultado.config(state='readonly', fg="#00cc00")
    detalle_label.config(text="", foreground="black")

ventana = tk.Tk()
ventana.title("Simulador de Venta")
ventana.geometry("500x600")
ventana.resizable(False, False)
ventana.configure(bg="WHITE")

style = ttk.Style()
style.theme_use("default")
style.configure("TLabel", font=("Arial", 11, "bold"), background="WHITE", foreground="DARK GREEN")
style.configure("TButton", font=("Arial", 11, "bold"), padding=6)
style.configure("TEntry", font=("Arial", 12, "bold"))

tk.Label(ventana, text="SIMULADOR DE VENTA", font=("Arial", 16, "bold"), bg="white", fg="LIGHT GREEN").pack(pady=(20, 10))

ttk.Label(ventana, text="Resultado final ($):", font=("Arial", 13, "bold")).pack(pady=(5, 5))
pantalla_resultado = tk.Entry(ventana, font=("Arial", 23, "bold"), justify="right", bd=6,
                              relief="ridge", state='readonly', bg="#f0fff0", fg="green")
pantalla_resultado.pack(pady=5, ipadx=10, ipady=15, fill='x', padx=30)

def crear_entrada(titulo, bind_formateo=False):
    ttk.Label(ventana, text=titulo).pack(pady=(15, 5))
    entry = ttk.Entry(ventana, justify="center")
    entry.pack(pady=5, padx=60, fill='x')
    if bind_formateo:
        entry.bind("<KeyRelease>", formatear_valor_producto)
    return entry

entry_base = crear_entrada("Valor del producto ($):", bind_formateo=True)
entry_comision1 = crear_entrada("Comisión por venta (%):")
entry_comision2 = crear_entrada("Anticipo de abono (%):")

var_iva_activado = tk.BooleanVar(value=True)
check_iva = ttk.Checkbutton(ventana, text="Aplicar IVA (19%)", variable=var_iva_activado)
check_iva.pack(pady=(20, 10))

boton_frame = tk.Frame(ventana, bg="white")
boton_frame.pack(pady=10)

ttk.Button(boton_frame, text="Calcular", command=calcular_descuento).grid(row=0, column=0, padx=10)
ttk.Button(boton_frame, text="Limpiar", command=limpiar_campos).grid(row=0, column=1, padx=10)

detalle_label = ttk.Label(ventana, text="", font=("Arial", 10), justify="left")
detalle_label.pack(pady=10, padx=30)

ventana.mainloop()
