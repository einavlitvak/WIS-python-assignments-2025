# Program to calculate the area of a trapeze
## option 1: input from terminal
def calculate_trapeze_area(base1, base2, height):
    """Calculate the area of a trapeze given its bases and height."""
    return 0.5 * (base1 + base2) * height

# Input parameters
print("Enter the parameters of the trapeze:")
base1 = float(input("Base 1: "))
base2 = float(input("Base 2: "))
height = float(input("Height: "))

# Calculate area
area = calculate_trapeze_area(base1, base2, height)

# Output result
print(f"The area of the trapeze is: {area}")

## option 2: predefined parameters in script
# Function to calculate the area with predefined parameters
def calculate_with_predefined_parameters():
    """Calculate the area of a trapeze using predefined parameters."""
    base1 = 10  # Example value for Base 1
    base2 = 15  # Example value for Base 2
    height = 7  # Example value for Height

    print("Calculating with predefined parameters...")
    print(f"Base 1: {base1}")
    print(f"Base 2: {base2}")
    print(f"Height: {height}")

    area = calculate_trapeze_area(base1, base2, height)
    print(f"The area of the trapeze is: {area}")

# Call the second function to calculate with predefined parameters
calculate_with_predefined_parameters()
