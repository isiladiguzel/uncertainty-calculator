import math

# --- RESULT FORMATTING ---
"""
Produces the final result with value ± uncertainty and optional unit.
Shown with 10 decimal places so that the user can round to desired significant figures manually, 10 decimals for the value as well(to be able to calculate very small quantities).
"""

def final_result(value, uncertainty, unit=""):
    if uncertainty < 0.001 or abs(value) >= 1e4:
        # Using scientific notation for very small uncertainty or large numbers.
        return f"{value:.10f} ± {uncertainty:.10f} {unit}".strip()
    else:
        return f"{value:.10f} ± {uncertainty:.10f} {unit}".strip()

"""
It uses scientific notation for very small uncertainties or large numbers.
It could also be changed to .2f, .1f depending on what sf is required. 3 sf was typically mentioned in my previous laboratory assignments and tests.

"""

# --- DIRECT MEASUREMENT UNCERTAINTY CALCULATIONS ---
def direct_measurement_uncertainty():
    """
    Computing uncertainty for a direct measurement.
    - If an uncertainty is already provided (e.g., from instrument specs/instructor), apply it directly.
    - Otherwise, estimate the uncertainty as (least_count / k).
    """
    print("\n Direct Measurement")
    value = float(input("Enter measured value: "))

    mode = input("Do you want to enter the uncertainty directly? (yes/no): ").strip().lower()

    if mode == "yes":
        # User supplies the provided uncertainty.
        uncertainty = float(input("Enter the measurement uncertainty: "))
    else:
        # Derive from smallest division using a divisor k
        least_count = float(input("Enter the instrument's smallest division (least count): "))
        k = float(input("Enter the divisor k : "))
        if k == 0:
            print(" Zero Error Division ")
            return
        uncertainty = least_count / k

    print(f"\nResult: {final_result(value, uncertainty)}")

# --- ADDITION / SUBTRACTION UNCERTAINTY CALCULATIONS ---
def addition_subtraction_uncertainty():
    print("\n Addition / Subtraction")
    a = float(input("Enter value A: "))
    delta_a = float(input("Enter uncertainty of A: "))
    b = float(input("Enter value B: "))
    delta_b = float(input("Enter uncertainty of B: "))
    operation = input("Choose operation (+ or -): ")

    if operation == "+":
        result = a + b
    elif operation == "-":
        result = a - b
    else:
        print("Invalid operation.")
        return

    total_uncertainty = abs(delta_a) + abs(delta_b)
    print(f"\nResult: {final_result(result, total_uncertainty)}")

"""
Uncertainty propagation for addition or subtraction:
Absolute uncertainties add: Δf = Δa + Δb (first-order, conservative).
"""




# --- MULTIPLICATION / DIVISION UNCERTAINTY CALCULATIONS ---

"""
Uncertainty propagation for multiplication or division (first-order linearization):
For f = a*b or f = a/b, the propagated absolute uncertainty is approximated by: Δf ≈ |∂f/∂a|Δa + |∂f/∂b|Δb
This is equivalent to adding relative uncertainties for products/ratios.
"""


def multiplication_division_uncertainty():
    print("\n Multiplication / Division")
    a = float(input("Enter value A: "))
    delta_a = float(input("Enter uncertainty of A: "))
    b = float(input("Enter value B: "))
    delta_b = float(input("Enter uncertainty of B: "))
    operation = input("Choose operation (* or /): ")



    if operation == "*":
        result = a * b
        total_uncertainty = abs(b) * abs(delta_a) + abs(a) * abs(delta_b)

    elif operation == "/":
        if b == 0:
            print("Division by Zero Error")
            return
        result = a / b
        total_uncertainty = (abs(delta_a) / abs(b)) + (abs(a) * abs(delta_b)) / (abs(b) ** 2)
    else:
        print("Invalid operation.")
        return

    print(f"\nResult: {final_result(result, total_uncertainty)}")

# --- OPTIONS ---

# A well-structured menu designed to clearly present calculation options to the user.

def main():
    options = {
        "1": direct_measurement_uncertainty,
        "2": addition_subtraction_uncertainty,
        "3": multiplication_division_uncertainty,
    }

    while True:
        print("\n Possible Options For Uncertainty Calculations\n"
              "1. Direct Measurement\n"
              "2. Addition / Subtraction\n"
              "3. Multiplication / Division\n"
              "4. Exit")

        choice = input("Select (1-4): ").strip()

        if choice == "4":
            print("Exiting on user request.")
            break

        func = options.get(choice)
        if func:
            func()
        else:
            print(" Please select 1-4. ")

main()