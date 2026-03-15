# All existing customers and their membership status
customers_data = dict({"Tim": True, "Rose": False})

# Services offered in the shop and their presets of service hours and parts requirement
shop_services = dict(
    inspection=tuple([1, False]),
    diagnostic=tuple([1, False]),
    maintenance=tuple([2, True]),
    repair=tuple([None, True]),
)

# Parts available in the shop for services and their prices in A$
parts_catalog = dict(
    oil=35,
    filter=25,
    brake=120,
    battery=180,
    radiator=420,
    motor=280,
)


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
    while True:
        name = input("Enter the name of the customer:\n")

        # If the name string has non-alphabetic characters or empty print an error message and then loop back
        for string in name.split():
            if not string.isalpha():
                print(
                    "The customer name is invalid. The name value contains non-alphabetic characters or is empty."
                )
                continue

        # Break when valid name is entered
        break

    # Lookup the customer name and then get their membership status
    if name in customers_data:
        is_member = customers_data[name]
    else:
        # Set membership flag to False for a new customer
        is_member = False

    return dict(name=name, is_member=is_member)


# Return a valid service request details including hours, parts, and costs
def get_service_details():
    # Loop until a vaild service is requested
    while True:
        service = input("Enter the service requested by the customer:\n")

        # If the service requested string is non-alphabetic or empty print an error message and then loop back
        if not service.isalpha():
            print(
                "The requested service is invalid. The service request cannot contain non-alphabetic characters or be empty."
            )
            continue
        # If the service is not offered by the shop print an error message and loop back
        elif service not in shop_services:
            print(
                "The requested service is invalid. The service requested is not offered at the shop."
            )
            continue

        # Break when valid service is requested
        break

    # Select the service preset
    service_preset = shop_services[service]

    # Get valid service hours if preset value is None
    if not service_preset[0]:
        while True:
            hours = input("Enter the number of hours required for the service:\n")

            # If the hours string is non-numeric or empty print an error message and then loop back
            for digits in hours.split("."):
                if not digits.isnumeric():
                    print(
                        "The hours entered for the service is invalid. The hours value cannot contain non-numeric characters or be empty."
                    )
                    continue

            # If hours string is not no a multiple of 0.5 print an error message and then loop back
            if float(hours) % 0.5 != 0:
                print(
                    "The hours entered for the service is invalid. The hours value should be in multiple of 0.5."
                )
                continue

            # Break when valid hours are entered
            break
    else:
        # Use default value if present
        hours = service_preset[0]

    # Get list of valid parts with their prices if they are required for the service
    parts = list()
    if service_preset[1]:
        while True:
            part = input(
                "Enter the part needed for the service [press enter to skip]:\n"
            )

            # Stop if no input is entered
            if not part:
                break
            # If the part name string is non-alphabetic print an error message and then loop back
            elif not part.isalpha():
                print(
                    "The part is invalid. The part name cannot contain non-alphabetic characters."
                )
                continue
            # If the part is not the catalog print an error message and loop back
            elif part not in parts_catalog:
                print(
                    "The part is invalid. The part entered does not exist in the catalog."
                )
                continue

            # Store part and its price
            parts.append(tuple([part, parts_catalog[part]]))

    # Return service details
    return dict(service=service, hours=hours, parts=parts)


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
    return dict(
        original_cost=original_cost,
        discount_amt=discount_amt,
        total_cost=total_cost,
        hourly_service_cost=SERVICE_COST,
    )


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

    # End printing receipt with section break
    print_receipt_line(is_section=True)


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
    RECEIPT_WIDTH = 75

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


perform_a_service()
