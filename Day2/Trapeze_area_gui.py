import tkinter as tk
from tkinter import messagebox

def calculate_trapeze_area(base1, base2, height):
    """Calculate the area of a trapeze given its bases and height."""
    return 0.5 * (base1 + base2) * height

def on_calculate():
    try:
        base1 = float(entry_base1.get())
        base2 = float(entry_base2.get())
        height = float(entry_height.get())

        if base1 <= 0 or base2 <= 0 or height <= 0:
            raise ValueError("All parameters must be positive numbers.")

        area = calculate_trapeze_area(base1, base2, height)
        label_result.config(text=f"Area: {area:.2f}")

        # Update trapeze image with arrows
        canvas.delete("all")
        canvas.create_polygon(50, 150, 150, 150, 120, 50, 80, 50, fill="lightblue", outline="blue")
        canvas.create_text(100, 160, text=f"Base 1: {base1}", fill="orange")
        canvas.create_text(100, 40, text=f"Base 2: {base2}", fill="orange")
        canvas.create_text(140, 100, text=f"Height: {height}", fill="orange")

    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))

# Create the main window
root = tk.Tk()
root.title("Trapeze Area Calculator")

# Input fields
frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Base 1:").grid(row=0, column=0, padx=5, pady=5)
entry_base1 = tk.Entry(frame_inputs)
entry_base1.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Base 2:").grid(row=1, column=0, padx=5, pady=5)
entry_base2 = tk.Entry(frame_inputs)
entry_base2.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Height:").grid(row=2, column=0, padx=5, pady=5)
entry_height = tk.Entry(frame_inputs)
entry_height.grid(row=2, column=1, padx=5, pady=5)

# Calculate button
btn_calculate = tk.Button(root, text="Calculate", command=on_calculate)
btn_calculate.pack(pady=10)

# Result label
label_result = tk.Label(root, text="Area: ", font=("Arial", 14))
label_result.pack(pady=10)

# Canvas for trapeze image
canvas = tk.Canvas(root, width=200, height=200, bg="white")
canvas.pack(pady=10)

# Run the application
root.mainloop()