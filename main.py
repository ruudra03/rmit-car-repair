# All existing customers and their membership status
customers_data = {"Tim": True, "Rose": False}

# Services offered in the shop and their presets of service hours and parts requirement
shop_services = {
    "inspection": (1, False),
    "diagnostic": (1, False),
    "maintenance": (2, True),
    "repair": (None, True),
}

# Parts available in the shop for services and their prices in A$
parts_catalog = {
    "oil": 35,
    "filter": 25,
    "brake": 120,
    "battery": 180,
    "radiator": 420,
    "motor": 280,
}


# Function that initiates the program
def start_program():
    # Print welcome message
    print("RMIT Car Repair Shop\n")

    # Keep running the program using a menu
    try:
        program_menu()
        # End the program once the function ends
        print("\nThe program has ended!")
    except EOFError:
        print("\nERROR! Program was ended abruptly.")


# Handle program options/features using menu
def program_menu():
    # Menu options available
    program_options = {
        1: ("Perform a service", perform_a_service),
        2: ("Update services", update_service_preset),
        3: ("Update parts", update_parts_catalog),
        4: ("Display existing customers", display_customers_data),
        5: ("Display existing services", display_shop_services),
        6: ("Display existing parts", display_parts_catalog),
    }

    # Handle relevant program feature based on user input
    is_program_running = True
    while is_program_running:
        print_program_menu(program_options)

        # Get option choice from user
        is_option_valid = False
        while not is_option_valid:
            choice = input("Enter an option: ")

            # Check if valid option is choosen
            try:
                choice_int = int(choice)

                # Quit the menu if 0 is entered
                if choice_int == 0:
                    is_option_valid = True
                    is_program_running = False
                    break

                # Get the option user choosed for and then call the associated function
                # Rerun the menu after the function is finished running
                for option_num, option in program_options.items():
                    if choice_int == option_num:
                        # Insert new line
                        print()
                        option[1]()
                        is_option_valid = True
                        break
            except ValueError:
                print("ERROR! Choose a valid option value from the menu.")
                continue


# Print program menu
def print_program_menu(program_options):
    # Menu separator string
    MENU_WIDTH = 75
    menu_separator_str = "#" * MENU_WIDTH

    # Print the menu with all the program options
    # Start the menu
    print(menu_separator_str)
    print("Program Menu")

    # Print program options
    for option_num, option in program_options.items():
        print(f"{option_num}: {option[0]}")

    # Add an option to quit the program and then end the menu
    print("[Enter '0' to exit the program]")
    print(menu_separator_str)


# Process a new service for a customer and then print a receipt in the end
def perform_a_service():
    # Get customer information who came in for service
    customer = get_customer()

    # Get service requested by the customer
    service_details = get_service_details()

    # Calculate service costs
    service_costs = get_service_costs(service_details, customer["is_member"])

    # Print a receipt for the service
    receipt_printer(service_details, service_costs)


# Return a valid customer name and their membership status
def get_customer():
    # Loop until a valid name is entered
    is_name_valid = False
    while not is_name_valid:
        name = input("Enter the name of the customer:\n")

        # If the name string has non-alphabetic characters or empty print an error message
        is_name_valid = validate_name_input(name)
        if not is_name_valid:
            print("ERROR! The customer's name should be non-empty and alphabetic.")

    # Lookup the customer name and then get their membership status
    if name in customers_data:
        is_member = customers_data[name]
    else:
        # Set membership flag to False for a new customer
        is_member = False

    return {"name": name, "is_member": is_member}


# Return a valid service request details including hours, parts, and costs
def get_service_details():
    # Loop until a vaild service is requested
    is_service_valid = False
    while not is_service_valid:
        service = input("Enter the service requested by the customer:\n")

        # If the service requested string is not offered by the shop or empty print an error message
        is_service_valid = validate_service_input(service)
        if not is_service_valid:
            print(
                "ERROR! The service request should be non-empty and available at the shop."
            )

    # Select the service preset
    service_preset = shop_services[service]

    # Get valid service hours if preset value is None
    if service_preset[0] is None:
        is_hours_valid = False
        while not is_hours_valid:
            hours = input("Enter the number of hours required for the service:\n")

            # If the hours string is non-numeric, zero, not a multiple of 0.5, or empty print an error message
            is_hours_valid = validate_hours_input(hours)
            if not is_hours_valid:
                print(
                    "ERROR! The hours should be non-zero, numeric, and a multiple of 0.5."
                )
    else:
        # Use default value if present
        hours = service_preset[0]

    # Get list of valid parts with their prices if they are required for the service
    parts = []
    if service_preset[1]:
        is_part_valid = False
        while not is_part_valid:
            part = input(
                "Enter the part needed for the service [Press enter to skip]:\n"
            )

            # If the input string is empty break out of the loop
            if not part:
                break

            # If the part name is not in the catalog print an error message
            is_part_valid = validate_part_input(part)
            if not is_part_valid:
                print("ERROR! The part entered should exist in the catalog.")
            else:
                # Store part and its price
                parts.append((part, parts_catalog[part]))

                # Continue looping until skipped
                is_part_valid = False

    # Return service details
    return {"service": service, "hours": hours, "parts": parts}


# Function that returns service hours, list of parts used and their prices, original cost, discount amount, and total cost
def get_service_costs(service_details, is_member):
    # Hourly rate (A$) of all services
    SERVICE_COST = 40.0

    # Membership discount rate
    MEMBERSHIP_DISCOUNT = 10

    # Calculate service charge based on hours spent
    service_charge = float(service_details["hours"]) * SERVICE_COST

    # Calculate the charge of parts used
    parts_charge = 0.0

    for part in service_details["parts"]:
        part_price = part[1]
        parts_charge += part_price

    # Calculate original cost of the service based on hours and parts expended
    original_cost = service_charge + parts_charge

    # Calculate discount amount based on customer's membership status
    if is_member:
        discount_amt = original_cost * (MEMBERSHIP_DISCOUNT / 100)
    else:
        discount_amt = 0.0

    # Calculate total cost after discount
    total_cost = original_cost - discount_amt

    # Return data required for the receipt printer
    return {
        "original_cost": original_cost,
        "discount_amt": discount_amt,
        "total_cost": total_cost,
        "hourly_service_cost": SERVICE_COST,
    }


# Print a receipt for a service using its details and costs
def receipt_printer(service_details, service_costs):
    # Start printing the receipt with its header
    print_receipt_line(is_header=True)

    # Print service charge
    print_receipt_line(
        is_body=True,
        left_string=service_details["service"],
        right_string=service_details["hours"],
        end_string=f" x {service_costs['hourly_service_cost']:.2f}",
    )

    # Print part charge
    for part in service_details["parts"]:
        print_receipt_line(
            is_body=True, left_string=part[0], right_string=f"{part[1]:.2f}"
        )

    # Add section break
    print_receipt_line(is_section=True)

    # Print original cost, discount amount, and total cost
    print_receipt_line(
        is_body=True,
        left_string="Original cost",
        right_string=f"{service_costs['original_cost']:.2f}",
        end_string=" (AUD)",
    )
    print_receipt_line(
        is_body=True,
        left_string="Discount",
        right_string=f"{service_costs['discount_amt']:.2f}",
        end_string=" (AUD)",
    )
    print_receipt_line(
        is_body=True,
        left_string="Total cost",
        right_string=f"{service_costs['total_cost']:.2f}",
        end_string=" (AUD)",
    )

    # End printing receipt with section break and a new line
    print_receipt_line(is_section=True)
    print()


# Helper function to handle text alignment of the formatted receipt
def print_receipt_line(
    is_header=False,
    is_section=False,
    is_body=False,
    left_string="",
    right_string="",
    end_string="",
):
    # Receipt paper width or characters space
    RECEIPT_WIDTH = 60

    # Section separator
    section_separator_str = "-" * RECEIPT_WIDTH

    # Check if section break is called
    if is_section:
        # Use section separator
        formatted_string = section_separator_str

    # Check if the text is to be aligned at center
    # Only use right side string
    if is_header:
        formatted_string = f"{section_separator_str}\n{'Receipt':^{RECEIPT_WIDTH}}\n{section_separator_str}"

    # Use left, right, and suffix strings if the text is body
    if is_body:
        # Set right side string's starting character position
        pos_right_str_at = RECEIPT_WIDTH - len(left_string) - len(end_string) - 1

        formatted_string = (
            f"{left_string}:{right_string:>{pos_right_str_at}}{end_string}"
        )

    print(formatted_string)


# Update service's hours preset
def update_service_preset():
    print("TODO")


# Update parts in the catalog
def update_parts_catalog():
    print("TODO")


# Display all the existing customers data
def display_customers_data():
    print("TODO")


# Display all the services offered at the shop
def display_shop_services():
    print("TODO")


# Display all the parts in the catalog
def display_parts_catalog():
    print("TODO")


# Validate customer name input
def validate_name_input(user_input):
    # Return False if string is empty
    if not user_input:
        return False

    # Get all separate strings from the name input
    strings = user_input.split()

    # If not all words are alphabetic return false
    for string in strings:
        if not string.isalpha():
            return False

    # If the input passes the check return True
    return True


# Validate service request input
def validate_service_input(user_input):
    # Return False if string is empty
    if not user_input:
        return False

    # If the service is not offered at the shop return False
    if user_input not in shop_services:
        return False

    # If the input passes the check return True
    return True


# Validate service hours input
def validate_hours_input(user_input):
    # Return False if string is empty
    if not user_input:
        return False

    # If hours is not float return False
    try:
        user_input_float = float(user_input)
    except ValueError:
        return False

    # If the value of hours entered is 0 or not a multiple of 0.5 return False
    if (user_input_float == 0) or (user_input_float % 0.5 != 0):
        return False

    # If the input passes the check return True
    return True


# Validate service part name input
def validate_part_input(user_input):
    # Return False if string is empty
    if not user_input:
        return False

    # If the part is not present in the catalog return False
    if user_input not in parts_catalog:
        return False

    # If the input passes the check return True
    return True


# Start the program
start_program()
