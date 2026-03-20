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

# Set program display width
PROGRAM_DISPLAY_WIDTH = 75


# Function that initiates the program
def start_program():
    separator_char = "="

    # Print welcome message
    print(f"{' RMIT Car Repair Shop ':{separator_char}^{PROGRAM_DISPLAY_WIDTH}}\n")

    # Keep running the program using a menu
    try:
        program_menu()
    except EOFError:
        print(f"\n\n{' Program Terminated ':{separator_char}^{PROGRAM_DISPLAY_WIDTH}}")
    else:
        # End the program once the program is quitted with '0'
        print(f"\n{' End of Program ':{separator_char}^{PROGRAM_DISPLAY_WIDTH}}")


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
        display_menu(program_options)

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
                elif choice_int in program_options:
                    # Get the option user choosed for and then call the associated function
                    # Rerun the menu after the function is finished running
                    # Insert new line
                    program_options[choice_int][1]()
                    is_option_valid = True
                else:
                    print("Invalid option. Please choose an option from the menu.")
            except ValueError:
                print("Invalid option. Please enter numeric values only.")
                continue


# Print program menu
def display_menu(program_options):
    # Menu separator string
    separator_char = "#"

    # Print the menu with all the program options
    # Start the menu
    print(separator_char * PROGRAM_DISPLAY_WIDTH)
    print(f"{'Program Menu':^{PROGRAM_DISPLAY_WIDTH}}")

    # Print program options
    for option_num, option in program_options.items():
        print(f"{option_num}: {option[0]}")

    # Add an option to quit the program and then end the menu
    print("Enter '0' to exit the program.")
    print(separator_char * PROGRAM_DISPLAY_WIDTH)


# Process a new service for a customer and then print a receipt in the end
def perform_a_service():
    # Get customer information who came in for service
    customer = get_customer()

    # Get service requested by the customer
    service_details = get_service_details()

    # Calculate service costs
    service_costs = get_service_costs(service_details, customer["is_member"])

    # Print a receipt for the service
    display_receipt(service_details, service_costs)


# Return a valid customer name and their membership status
def get_customer():
    # Loop until a valid name is entered
    while True:
        name = input("Enter customer name: ")

        # If the name string has non-alphabetic characters or empty print an error message
        if validate_name_input(name):
            break
        else:
            print("Invalid name. Please enter alphabetic characters only.")

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
    while True:
        service = input("Enter service requested: ")

        # If the service requested string is not offered by the shop or empty print an error message
        if validate_service_input(service):
            # Select the service preset
            service_preset = shop_services[service]
            break
        else:
            print("Invalid service. Please request a service available at the shop.")

    # Get valid service hours if preset value is None
    if service_preset[0] is None:
        while True:
            hours = input("Enter hours required: ")

            # If the hours string is non-numeric, zero, not a multiple of 0.5, or empty print an error message
            if validate_hours_input(hours):
                break
            else:
                print(
                    "Invalid hours. Please enter a positive number in multiples of 0.5."
                )
    else:
        # Use default value
        hours = service_preset[0]

    # Get list of valid parts with their prices if they are required for the service
    parts = []
    if service_preset[1]:
        while True:
            part = input("Enter part required [press enter to skip]: ")

            # If the input string is empty and at least one part has been entered break out of the loop
            if not part and parts:
                break
            elif validate_part_input(part):
                # Store part and its price
                parts.append((part, parts_catalog[part]))
                continue
            else:
                print("Invalid part. Please enter a part from the catalog.")

    # Return service details
    return {"service": service, "hours": hours, "parts": parts}


# Function that returns service hours, list of parts used and their prices, original cost, discount amount, and total cost
def get_service_costs(service_details, is_member):
    # Hourly rate (A$) of all services
    HOURLY_SERVICE_COST = 40.0

    # Membership discount rate
    MEMBERSHIP_DISCOUNT = 10

    # Calculate service charge based on hours spent
    service_charge = float(service_details["hours"]) * HOURLY_SERVICE_COST

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
        "hourly_service_cost": HOURLY_SERVICE_COST,
    }


# Print a receipt for a service using its details and costs
def display_receipt(service_details, service_costs):
    # Section separator
    separator_char = "-"

    # Column details
    num_of_cols = 2  # left and right columns
    col_width = PROGRAM_DISPLAY_WIDTH // num_of_cols
    receipt_display_width = num_of_cols * col_width

    # Start printing the receipt with its header
    print(
        f"{separator_char * receipt_display_width}\n{'Receipt':^{receipt_display_width}}\n{separator_char * receipt_display_width}"
    )

    # Print service charge
    print(
        f"{service_details['service'] + ':':<{col_width}}{service_details['hours'] + f' x {service_costs['hourly_service_cost']:.2f}':>{col_width}}"
    )

    # Print part charge
    for part in service_details["parts"]:
        print(f"{part[0] + ':':<{col_width}}{f'{part[1]:.2f}':>{col_width}}")

    # Add section break
    print(separator_char * receipt_display_width)

    # Print original cost, discount amount, and total cost
    print(
        f"{'Original Cost':<{col_width}}{f'{service_costs['original_cost']:.2f}' + ' (AUD)':>{col_width}}"
    )

    print(
        f"{'Discount':<{col_width}}{f'{service_costs['discount_amt']:.2f}' + ' (AUD)':>{col_width}}"
    )

    print(
        f"{'Total Cost':<{col_width}}{f'{service_costs['total_cost']:.2f}' + ' (AUD)':>{col_width}}"
    )

    # End printing receipt with section break
    print(separator_char * receipt_display_width)


# Update service's hours preset
def update_service_preset():
    print("TODO")


# Update parts in the catalog
def update_parts_catalog():
    print("TODO")


# Display all the existing customers data
def display_customers_data():
    # Section separator
    separator_char = "-"

    customers_data_cols = [("No.", 5), ("Customer name", 15), ("Member", 8)]

    # Add section break
    print(separator_char * PROGRAM_DISPLAY_WIDTH)

    # Print header
    headers_row = ""

    for col_header, col_width in customers_data_cols:
        headers_row += f"{col_header:<{col_width}}"
    print(headers_row)

    # Print each customer
    customer_count = 0
    for customer in customers_data:
        customer_row = ""

        customer_count += 1
        customer_row += f"{customer_count:<{customers_data_cols[0][1]}}"

        # Add customer name column data
        customer_row += f"{customer:<{customers_data_cols[1][1]}}"

        # Add member column data
        # Convert membership flags True or Flase to Yes or No respectively
        if customers_data[customer] is True:
            customer_row += f"{'Yes':<{customers_data_cols[2][1]}}"
        else:
            customer_row += f"{'No':<{customers_data_cols[2][1]}}"

        print(customer_row)

    # Add section break
    print(separator_char * PROGRAM_DISPLAY_WIDTH)


# Display all the services offered at the shop
def display_shop_services():
    # Section separator
    separator_char = "-"

    shop_services_cols = [
        ("Service", 13),
        ("Service hours", 15),
        ("Hours input required", 22),
        ("Parts input required", 22),
    ]

    # Add section break
    print(separator_char * PROGRAM_DISPLAY_WIDTH)

    # Print header
    headers_row = ""
    for col_header, col_width in shop_services_cols:
        headers_row += f"{col_header:<{col_width}}"
    print(headers_row)

    # Print each service available in the shop
    for service in shop_services:
        service_row = ""

        # Add service name column data
        service_row += f"{service:<{shop_services_cols[0][1]}}"

        # Select the service preset
        service_preset = shop_services[service]

        # Add hours and hours input required column data
        # Check if hour preset is None
        service_hours = service_preset[0]
        if service_hours is None:
            service_row += f"{'Input Value':<{shop_services_cols[1][1]}}"
            service_row += f"{'Yes':<{shop_services_cols[2][1]}}"
        else:
            if service_hours < 1:
                service_row += (
                    f"{str(service_hours) + ' hour':<{shop_services_cols[1][1]}}"
                )
            else:
                service_row += (
                    f"{str(service_hours) + ' hours':<{shop_services_cols[1][1]}}"
                )
            service_row += f"{'No':<{shop_services_cols[2][1]}}"

        # Add parts required column data
        # Convert parts required flags True or Flase to Yes or No respectively
        if service_preset[1] is True:
            service_row += f"{'Yes':<{shop_services_cols[3][1]}}"
        else:
            service_row += f"{'No':<{shop_services_cols[3][1]}}"

        print(service_row)

    # Add section break
    print(separator_char * PROGRAM_DISPLAY_WIDTH)


# Display all the parts in the catalog
def display_parts_catalog():
    # Section separator
    separator_char = "-"

    parts_catalog_cols = [("Part", 10), ("Price (AUD)", 13)]

    # Add section break
    print(separator_char * PROGRAM_DISPLAY_WIDTH)

    # Print header
    headers_row = ""
    for col_header, col_width in parts_catalog_cols:
        headers_row += f"{col_header:<{col_width}}"
    print(headers_row)

    # Print each part
    for part in parts_catalog:
        part_row = ""

        # Add part name column data
        part_row += f"{part:<{parts_catalog_cols[0][1]}}"

        # Add part price column data
        part_row += f"{f'{parts_catalog[part]:.2f}':<{parts_catalog_cols[1][1]}}"

        print(part_row)

    # Add section break
    print(separator_char * PROGRAM_DISPLAY_WIDTH)


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
    if (user_input_float <= 0) or (user_input_float % 0.5 != 0):
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
