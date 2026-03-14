# Customers and their membership status
# Initialise with two customers
customers_data = dict(tim=True, rose=False)

# Services offered and their presets of service hours and parts requirement
shop_services = dict(
    inspection=tuple([1.0, False]),
    diagnostic=tuple([1.0, False]),
    maintenance=tuple([2.0, True]),
    repair=tuple([None, True]),
)

# Parts available and their prices (A$)
parts_catalog = dict(
    oil=35.0,
    filter=25.0,
    brake=120.0,
    battery=180.0,
    radiator=420.0,
    motor=280.0,
)


# Function to initialise a new service for a customer and print a receipt
def perform_a_service():
    # Get the name of the customer who came in for service
    customer_name = input("Enter the customer's name:\n")

    # Lookup the customer name and then get their membership status
    if customer_name in customers_data:
        is_member = customers_data[customer_name]
    else:
        # Set membership flag to False for a new customer
        is_member = False

    # Get service requested by the customer
    service_req = input("Choose the type of service requested by the customer:\n")

    # Get hours required to finish the service and check whether the requested service requires any parts
    service_hours = shop_services[service_req][0]
    is_part_required = shop_services[service_req][1]

    # Get service hours if preset value is None
    if not service_hours:
        service_hours = float(
            input(f"How many hours do you need for the {service_req}?\n")
        )

    # Get list of all parts needed for the service if necessary
    parts_list = list()

    while is_part_required:
        part = input(
            f"Which part do you want to use for the {service_req}? (Press enter to skip)\n"
        )

        # Check if part name is entered
        if part:
            parts_list.append(part)
        else:
            break

    # Calculate service costs and form its data
    service_data = set_service_data(service_req, service_hours, parts_list, is_member)

    # Print a receipt for the service
    receipt_printer(service_data)


# Function that returns service hours, list of parts used and their prices, original cost, discount amount, and total cost
def set_service_data(service_req, service_hours, parts_list, is_member):
    # Hourly rate (A$) of all services
    SERVICE_COST = 40.0

    # Membership discount rate
    MEMBERSHIP_DISCOUNT = 10

    # Calculate service charge based on hours spent
    service_charge = service_hours * SERVICE_COST

    # Calculate the charge of parts used and record their individual prices
    service_parts = set()
    parts_charge = 0.0

    for part in parts_list:
        part_price = parts_catalog[part]

        service_parts.add(tuple([part, part_price]))
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
        service=service_req,
        hours=service_hours,
        parts=service_parts,
        original_cost=original_cost,
        discount_amt=discount_amt,
        total_cost=total_cost,
        hourly_service_cost=SERVICE_COST,
    )


# Prints a receipt for a service using its type, hours, and parts if necessary
def receipt_printer(service_data):
    # Start printing the receipt with its header
    printer_line(is_header=True)

    # Print service charge
    printer_line(
        is_body=True,
        left_string=service_data["service"],
        right_string=service_data["hours"],
        end_string=f" x {service_data['hourly_service_cost']}",
    )

    # Print part charge
    for part in service_data["parts"]:
        printer_line(is_body=True, left_string=part[0], right_string=part[1])

    # Add section break
    printer_line(is_section=True)

    # Print original cost, discount amount, and total cost
    printer_line(
        is_body=True,
        left_string="Original cost",
        right_string=service_data["original_cost"],
        end_string=" (AUD)",
    )
    printer_line(
        is_body=True,
        left_string="Discount",
        right_string=service_data["discount_amt"],
        end_string=" (AUD)",
    )
    printer_line(
        is_body=True,
        left_string="Total cost",
        right_string=service_data["total_cost"],
        end_string=" (AUD)",
    )

    # End printing receipt with section break
    printer_line(is_section=True)


# Helper function to handle text alignment of the formatted receipt
def printer_line(
    is_header=False,
    is_section=False,
    is_body=False,
    left_string="",
    right_string="",
    end_string="",
):
    # Receipt paper width or characters space
    RECEIPT_WIDTH = 75

    # Section seperator
    section_seperator_str = "-" * RECEIPT_WIDTH

    # Check if section break is called
    if is_section:
        # Use section seperator
        formatted_string = section_seperator_str

    # Check if the text is to be aligned at center
    # Only use right side string
    if is_header:
        formatted_string = f"{section_seperator_str}\n{'Receipt':^{RECEIPT_WIDTH}}\n{section_seperator_str}"

    # Use left, right, and suffix strings if the text is body
    if is_body:
        # Set right side string's starting character position
        pos_right_str_at = RECEIPT_WIDTH - len(left_string) - len(end_string) - 1

        formatted_string = (
            f"{left_string}:{right_string:>{pos_right_str_at}}{end_string}"
        )

    print(formatted_string)


perform_a_service()
