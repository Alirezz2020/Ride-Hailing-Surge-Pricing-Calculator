def is_peak_hour(current_time):
    """
    Define peak hours as 7-9 AM and 5-7 PM.
    """
    return current_time.hour in [7, 8, 17, 18]

def calculate_surge_multiplier(demand, supply, current_time, event=False):
    """
    Calculate the surge multiplier based on:
      - Demand vs. Supply ratio
      - Whether it's peak hour
      - Special events
    """
    surge_multiplier = 1.0

    # If no drivers are available, apply an extreme surge multiplier
    if supply == 0:
        return 3.0

    ratio = demand / supply
    if ratio > 1:
        # Increase multiplier gradually based on demand-supply gap
        surge_multiplier += (ratio - 1) * 0.5

    # Boost multiplier during peak hours
    if is_peak_hour(current_time):
        surge_multiplier *= 1.2

    # Further boost multiplier if there's a special event
    if event:
        surge_multiplier *= 1.5

    return round(surge_multiplier, 2)
