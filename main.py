# List of all the customers and their membership status
store_customers = dict(tim=True, rose=False)  # initialise with two customers

# List of all services available including their service hours and whether they require parts to finish
store_services = dict(
    [
        ("inspection", [1.0, False]),
        ("diagnostic", [1.0, False]),
        ("maintenance", [2.0, True]),
        ("repair", [None, True]),
    ]
)

# List of all parts and their prices (in A$)
store_parts = dict(
    oil=35.0,
    filter=25.0,
    brake=120.0,
    battery=180.0,
    radiator=420.0,
    motor=280.0,
)

# Service cost per hour (in A$) for all jobs
SERVICE_COST_PER_HOUR = 40.0


# Formula to calculate original cost of a job (i.e., excluding member's discount)
def calc_original_cost(hours, parts):
    # Cost based on service hours
    service_cost = hours * SERVICE_COST_PER_HOUR

    # Cost of parts required for the job
    parts_cost = store_parts[parts]

    # Calculate orignal cost
    original_cost = service_cost + parts_cost

    # Return original cost
    return original_cost


# Ask for customer's name
customer_name = input("Enter the customer's name:\n")

# Ask for the type of service requested by the customer
service_requested = input("Choose the type of service requested by the customer:\n")

# Get presets of the requested job
service_hours = store_services[service_requested][0]
service_parts = store_services[service_requested][1]

# Ask for the total service hours required to finish the job
if not service_hours:
    service_hours = float(
        input(f"How many hours are required for the {service_requested}?\n")
    )

# Ask for parts required for the job
if service_parts:
    service_parts = input(f"Which part do you need for the {service_requested}?\n")

# Calculate the total cost for the specific job
original_cost = calc_original_cost(service_hours, service_parts)

print(original_cost)
