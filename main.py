# All existing customers and their membership status
customers = {"tim": True, "rose": False}

# Services offered in the shop and their presets of service hours and parts requirement
services = {
    "inspection": {"service_hours": 1, "is_part_required": False},
    "diagnostic": {"service_hours": 1, "is_part_required": False},
    "maintenance": {"service_hours": 2, "is_part_required": True},
    "repair": {"service_hours": None, "is_part_required": True},
}

# Parts available in the shop for services and their prices in A$
parts = {
    "oil": 35.0,
    "filter": 25.0,
    "brake": 120.0,
    "battery": 180.0,
    "radiator": 420.0,
    "motor": 280.0,
}

# Set program display width
DISPLAY_WIDTH = 70

# Set separator charcters
DIVIDER_CHAR = "-"
MENU_SECTION_CHAR = "="
START_AND_END_CHAR = "#"


# Function that initiates the program
def start():
    # Print welcome message
    print(START_AND_END_CHAR * DISPLAY_WIDTH)
    print(f"{'RMIT Car Repair Shop':^{DISPLAY_WIDTH}}")
    print(START_AND_END_CHAR * DISPLAY_WIDTH)

    # Keep running the program using a menu
    try:
        run_menu()
    except EOFError:
        print("\n" + START_AND_END_CHAR * DISPLAY_WIDTH)
        print(f"{'Program Terminated':^{DISPLAY_WIDTH}}")
        print(START_AND_END_CHAR * DISPLAY_WIDTH)
    else:
        # End the program once the program is quitted with '0'
        print(START_AND_END_CHAR * DISPLAY_WIDTH)
        print(f"{'End of Program':^{DISPLAY_WIDTH}}")
        print(START_AND_END_CHAR * DISPLAY_WIDTH)


# Handle program options/features using menu
def run_menu():
    # Menu options available
    options = {
        1: ("Perform a service", perform_a_service),
        2: ("Update services", update_service_preset),
        3: ("Update parts", update_parts_catalog),
        4: ("Display existing customers", display_existing_customers),
        5: ("Display existing services", display_existing_services),
        6: ("Display existing parts", display_existing_parts),
    }

    # Handle relevant program feature based on user input
    while True:
        display_menu(options)

        # Get option choice from user
        while True:
            # Check if valid option is choosen
            try:
                choice = int(input("Enter an option: ").strip())
            except ValueError:
                print("\nInvalid option! Enter numeric characters only.")
                continue

            # Quit the menu if 0 is entered
            if choice == 0:
                return
            elif choice in options:
                # Get the option user choosed for and then call the associated function
                # Display the menu again after the function is finished running
                print()  # Print new line
                options[choice][1]()
                break
            else:
                print("\nInvalid option! Enter a valid option from the menu.")


# Print program menu
def display_menu(options):
    # Print the menu with all the program options
    # Start the menu
    print("\n" + MENU_SECTION_CHAR * DISPLAY_WIDTH)
    print(f"{'MENU':^{DISPLAY_WIDTH}}")

    # Print program options
    for option, (label, _) in options.items():
        print(f"{option}: {label}")

    # Add an option to quit the program and then end the menu
    print("0: Exit program")
    print(MENU_SECTION_CHAR * DISPLAY_WIDTH)


# Process a new service for a customer and then print a receipt in the end
def perform_a_service():
    # Get customer information who came in for service
    customer = get_customer_details()

    # Get service requested by the customer
    service = get_service_details()

    # Calculate service costs
    costs = calculate_costs(service, customer["is_member"])

    # Print a receipt for the service
    display_receipt(service, costs)


# Return a valid customer name and their membership status
def get_customer_details():
    # Loop until a valid name is entered
    while True:
        # Get all the separate words from the name input
        name = input("Enter customer name: ").strip().lower()

        # If name is empty print an error message and loop back
        if not name:
            print("\nInvalid name! Enter a valid name.")
            continue

        # If not all words are alphabetic print an error message and loop back
        if not all(word.isalpha() for word in name.split()):
            print("\nInvalid name! Enter alphabetic characters only.")
            continue

        # Break if a valid name is entered
        break

    # Lookup the customer name and then get their membership status
    if customers.get(name):
        has_record = True
        is_member = customers[name]
    else:
        # Set record and membership flag to False for a new customer
        has_record = False
        is_member = False

    return {"name": name, "has_record": has_record, "is_member": is_member}


# Return a valid service request details including hours, parts, and costs
def get_service_details():
    # Loop until a vaild service is requested
    while True:
        service = input("Enter service: ").strip().lower()

        if services.get(service):
            service_info = services[service]

            # Get service hours
            if service_info["service_hours"]:
                service_hours = service_info["service_hours"]
            else:
                service_hours = get_service_hours()

            if service_info["is_part_required"]:
                service_parts = get_service_parts()
            else:
                service_parts = []

            # Return service details
            return {
                "service": service,
                "service_hours": service_hours,
                "service_parts": service_parts,
            }
        else:
            # If the service requested string is not offered by the shop or empty print an error message and loop back
            print("\nInvalid service! Enter a service available.")
            continue


# Get service hours
def get_service_hours():
    # Get valid service hours
    while True:
        service_hours = input("Enter hours: ").strip()

        try:
            service_hours = float(service_hours)
        except ValueError:
            # If the hours string is non-numeric or empty print an error message and loop back
            print("\nInvalid hours! Enter numeric characters only.")
            continue

        if (service_hours > 0) and (service_hours % 0.5 == 0):
            return service_hours
        else:
            print("\nInvalid hours! Enter a positive number in increments of 0.5.")
            continue


# Get service parts
def get_service_parts():
    service_parts = []
    while True:
        # If at least one part is already entered
        if service_parts:
            part = input("Enter part (press Enter to finish): ").strip().lower()
        else:
            part = input("Enter part: ").strip().lower()

        # If part input is non-empty then lookup for the part
        if part:
            if parts.get(part):
                service_parts.append((part, parts[part]))
                continue
            else:
                print("\nInvalid part! Enter a part available.")
                continue
        else:
            if service_parts:
                # Finish entering parts
                return service_parts
            else:
                # If no part is entered yet print an error message and loop back
                print("\nInvalid part! Enter at least one part.")
                continue


# Function that returns service hours, list of parts used and their prices, original cost, discount amount, and total cost
def calculate_costs(service, is_member):
    # Hourly rate (A$) of all services
    HOURLY_SERVICE_RATE = 40

    # Membership discount rate
    MEMBER_DISCOUNT = 10

    # Calculate service cost based on hours spent
    service_cost = service["service_hours"] * HOURLY_SERVICE_RATE

    # Calculate the cost of parts used
    parts_cost = 0
    for _, price in service["service_parts"]:
        parts_cost += price

    # Calculate original cost of the service based on hours and parts expended
    original_cost = service_cost + parts_cost

    # Calculate discount amount based on customer's membership status
    if is_member:
        discount = original_cost * (MEMBER_DISCOUNT / 100)
    else:
        discount = 0

    # Calculate total cost after discount
    total_cost = original_cost - discount

    # Return data required for the receipt printer
    return {
        "original_cost": original_cost,
        "discount": discount,
        "total_cost": total_cost,
        "hourly_service_rate": HOURLY_SERVICE_RATE,
    }


# Print a receipt for a service using its details and costs
def display_receipt(service, costs):
    # Column and width details
    receipt_width = 60
    column_width = receipt_width // 2  # Using two columns

    # Start printing the receipt with its header
    print("\n" + DIVIDER_CHAR * receipt_width)
    print(f"{'Receipt':^{receipt_width}}")
    print(DIVIDER_CHAR * receipt_width)

    # Print service charge
    print_receipt_line(
        f"{service['service'].capitalize()}:",
        f"{service['service_hours']} x {costs['hourly_service_rate']:.2f}",
        column_width,
    )

    # Print part charge
    for part, price in service["service_parts"]:
        print_receipt_line(
            f"{part.capitalize()}:",
            f"{price:.2f}",
            column_width,
        )

    # Add section break
    print(DIVIDER_CHAR * receipt_width)

    # Print original cost, discount amount, and total cost
    print_receipt_line(
        f"{'Original Cost:'}",
        f"{costs['original_cost']:.2f} AUD",
        column_width,
    )

    print_receipt_line(
        f"{'Discount:'}",
        f"{costs['discount']:.2f} AUD",
        column_width,
    )

    print_receipt_line(
        f"{'Total Cost:'}",
        f"{costs['total_cost']:.2f} AUD",
        column_width,
    )

    # End printing receipt with section break
    print(DIVIDER_CHAR * receipt_width)


# Print receipt line
def print_receipt_line(left_column, right_column, column_width):
    print(f"{left_column:<{column_width}}{right_column:>{column_width}}")


# Update service's hours preset
def update_service_preset():
    print("TODO")


# Update parts in the catalog
def update_parts_catalog():
    print("TODO")


# Display all the existing customers data
def display_existing_customers():
    columns = [("No.", 5), ("Customer name", 15), ("Member", 8)]
    total_col_width = 28

    print_data_header(columns, total_col_width)

    # Print each customer
    for index, (name, is_member) in enumerate(customers.items(), start=1):
        # Convert membership flags True or Flase to Yes or No respectively
        member = "Yes" if is_member else "No"

        row = f"{index:<{columns[0][1]}}{name.capitalize():<{columns[1][1]}}{member:<{columns[2][1]}}"

        print(row)

    # Add section break
    print(DIVIDER_CHAR * total_col_width)


# Display all the services offered at the shop
def display_existing_services():
    columns = [
        ("Service", 13),
        ("Service hours", 13),
        ("Hours input required", 22),
        ("Parts input required", 22),
    ]
    total_col_width = 70

    print_data_header(columns, total_col_width)

    # Print each service available in the shop
    for service, service_info in services.items():
        service_hours = service_info["service_hours"]
        is_part_required = service_info["is_part_required"]

        if service_hours:
            service_hours = str(service_hours) + " hour(s)"
            hours_input_reuired = "No"
        else:
            service_hours = "User-input"
            hours_input_reuired = "Yes"

        parts_input_required = "Yes" if is_part_required else "No"

        row = f"{service.capitalize():<{columns[0][1]}}{service_hours:<{columns[1][1]}}{hours_input_reuired:<{columns[2][1]}}{parts_input_required:<{columns[3][1]}}"

        print(row)

    # Add section break
    print(DIVIDER_CHAR * total_col_width)


# Display all the parts in the catalog
def display_existing_parts():
    columns = [("Part", 10), ("Price (AUD)", 13)]
    total_col_width = 23

    print_data_header(columns, total_col_width)

    # Print each part
    for part, price in parts.items():
        # Add part name column data
        row = f"{part.capitalize():<{columns[0][1]}}{f'{price:.2f}':<{columns[0][1]}}"

        print(row)

    # Add section break
    print(DIVIDER_CHAR * total_col_width)


# Print data headers
def print_data_header(columns, total_col_width):
    print(DIVIDER_CHAR * total_col_width)

    # Print header
    header = ""
    for column, width in columns:
        header += f"{column:<{width}}"
    print(header)

    # Add section break
    print(DIVIDER_CHAR * total_col_width)


# Start the program
start()
