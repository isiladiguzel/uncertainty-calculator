# --- RESULT FORMATTING ---

import math

"""
Produces the final result with value ± uncertainty. 

The uncertainty is rounded to 1 significant figure,
or 2 significant figures if the leading digit is 1.

The value is rounded to the same decimal place as the uncertainty.
"""


def round_uncertainty(uncertainty):
    if uncertainty == 0:
        return 0, 0

    exponent = math.floor(math.log10(abs(uncertainty)))
    first_digit = int(abs(uncertainty) / (10**exponent))

    if first_digit == 1:
        sig_figs = 2
    else:
        sig_figs = 1

    decimal_places = sig_figs - 1 - exponent
    rounded_uncertainty = round(uncertainty, decimal_places)

    return rounded_uncertainty, decimal_places


def final_result(value, uncertainty, unit=""):
    rounded_uncertainty, decimal_places = round_uncertainty(uncertainty)
    rounded_value = round(value, decimal_places)

    if decimal_places >= 0:
        return f"{rounded_value:.{decimal_places}f} ± {rounded_uncertainty:.{decimal_places}f} {unit}".strip()
    else:
        return f"{rounded_value:.0f} ± {rounded_uncertainty:.0f} {unit}".strip()


# --- DIRECT MEASUREMENT UNCERTAINTY CALCULATIONS ---


def direct_measurement_uncertainty():
    """
    Computing uncertainty for a direct measurement.
    - If an uncertainty is already provided (e.g., from instrument specs/instructor), apply it directly.
    - Otherwise, estimate the uncertainty as (least_count / k).
    """
    print("\n Direct Measurement")

    try:
        value = float(input("Enter measured value: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    mode = input("Do you want to enter the uncertainty directly? (yes/no): ").strip().lower()

    if mode == "yes" or mode == "y":
        try:
            uncertainty = float(input("Enter the measurement uncertainty: "))
        except ValueError:
            print("Please enter a valid number.")
            return

        if uncertainty < 0:
            print("Uncertainty cannot be negative.")
            return

    else:
        # Derive from the smallest division using a divisor k
        try:
            least_count = float(input("Enter the instrument's smallest division (least count): "))
            k = float(input("Enter the divisor k : "))
        except ValueError:
            print("Please enter a valid number.")
            return

        if k == 0:
            print(" Zero Error Division ")
            return

        uncertainty = least_count / k

        if uncertainty < 0:
            print("Uncertainty cannot be negative.")
            return

    print(f"\nResult: {final_result(value, uncertainty)}")


# --- ADDITION / SUBTRACTION UNCERTAINTY CALCULATIONS ---


def addition_subtraction_uncertainty():
    print("\n Addition / Subtraction")

    try:
        a = float(input("Enter value A: "))
        delta_a = float(input("Enter uncertainty of A: "))
        b = float(input("Enter value B: "))
        delta_b = float(input("Enter uncertainty of B: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    if delta_a < 0 or delta_b < 0:
        print("Uncertainty cannot be negative.")
        return

    operation = input("Choose operation (+ or -): ")

    if operation == "+":
        result = a + b
    elif operation == "-":
        result = a - b
    else:
        print("Invalid operation.")
        return

    total_uncertainty = (delta_a**2 + delta_b**2)**0.5

    print(f"\nResult: {final_result(result, total_uncertainty)}")


"""
Uncertainty propagation for addition or subtraction using the quadrature method:

Δf = sqrt((Δa)^2 + (Δb)^2)
"""


# --- MULTIPLICATION / DIVISION UNCERTAINTY CALCULATIONS ---

"""
Uncertainty propagation for multiplication or division using the quadrature method:

Δf / |f| = sqrt((Δa / a)^2 + (Δb / b)^2)
"""


def multiplication_division_uncertainty():
    print("\n Multiplication / Division")

    try:
        a = float(input("Enter value A: "))
        delta_a = float(input("Enter uncertainty of A: "))
        b = float(input("Enter value B: "))
        delta_b = float(input("Enter uncertainty of B: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    if delta_a < 0 or delta_b < 0:
        print("Uncertainty cannot be negative.")
        return

    operation = input("Choose operation (* or /): ")

    if a == 0 or b == 0:
        print("Invalid operation: values cannot be zero.")
        return

    if operation == "*":
        result = a * b
        total_uncertainty = abs(result) * (
            ((delta_a / a)**2 + (delta_b / b)**2)**0.5
        )

    elif operation == "/":
        result = a / b
        total_uncertainty = abs(result) * (
            ((delta_a / a)**2 + (delta_b / b)**2)**0.5
        )

    else:
        print("Invalid operation.")
        return

    print(f"\nResult: {final_result(result, total_uncertainty)}")


# --- ADDITIONAL CALCULATIONS ---

def power_uncertainty():
    print("\n Power")

    try:
        a = float(input("Enter value A: "))
        delta_a = float(input("Enter uncertainty of A: "))
        n = float(input("Enter exponent n: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    if delta_a < 0:
        print("Uncertainty cannot be negative.")
        return

    if a == 0:
        print("Invalid operation: value A cannot be zero.")
        return

    result = a**n
    relative_uncertainty = abs(n) * (delta_a / abs(a))
    total_uncertainty = abs(result) * relative_uncertainty

    print(f"\nResult: {final_result(result, total_uncertainty)}")


"""
Uncertainty propagation for powers:

q = a^n
u(q) / q = |n| * u(a) / a
"""


def logarithm_uncertainty():
    print("\n Natural Logarithm")

    try:
        a = float(input("Enter value A: "))
        delta_a = float(input("Enter uncertainty of A: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    if delta_a < 0:
        print("Uncertainty cannot be negative.")
        return

    if a <= 0:
        print("Invalid operation: value A must be greater than zero.")
        return

    result = math.log(a)
    total_uncertainty = delta_a / a

    print(f"\nResult: {final_result(result, total_uncertainty)}")


"""
Uncertainty propagation for natural logarithm:

q = ln(a)
u(q) = u(a) / a
"""


# --- OPTIONS ---

# A well-structured menu designed to clearly present calculation options to the user.

def main():
    options = {
        "1": direct_measurement_uncertainty,
        "2": addition_subtraction_uncertainty,
        "3": multiplication_division_uncertainty,
        "4": power_uncertainty,
        "5": logarithm_uncertainty,
    }

    while True:
        print(
            "\n Possible Options For Uncertainty Calculations\n"
            "1. Direct Measurement\n"
            "2. Addition / Subtraction\n"
            "3. Multiplication / Division\n"
            "4. Power\n"
            "5. Natural Logarithm\n"
            "6. Exit"
        )

        choice = input("Select (1-6): ").strip()

        if choice == "6":
            print("Exiting on user request.")
            break

        func = options.get(choice)

        if func:
            func()
        else:
            print(" Please select 1-6. ")


if __name__ == "__main__":
    main()
