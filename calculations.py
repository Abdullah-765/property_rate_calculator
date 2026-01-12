# calculations.py

STAMP_DUTY_PERCENTAGE = 2 / 100
SELLER_7E_PERCENTAGE = 1 / 100


def calculate_dc_value(area, dc_rate):
    return area * dc_rate


def calculate_fbr_value(area, fbr_rate):
    return area * fbr_rate


def calculate_rebate(fbr_value, rebate_percentage):
    if rebate_percentage > 0:
        return (rebate_percentage / 100) * fbr_value
    return 0


def calculate_advance_tax(value):
    if value <= 50_000_000:
        return (1.5 / 100) * value, 1.5
    elif value <= 100_000_000:
        return (2 / 100) * value, 2
    return (2.5 / 100) * value, 2.5


def calculate_gain_tax(value):
    if value <= 50_000_000:
        return (4.5 / 100) * value, 4.5
    elif value <= 100_000_000:
        return (5 / 100) * value, 5
    return (5.5 / 100) * value, 5.5


def calculate_stamp_duty(dc_value):
    return STAMP_DUTY_PERCENTAGE * dc_value


def calculate_seller_7e(value):
    return SELLER_7E_PERCENTAGE * value


def calculate_town_tax(dc_value):
    return (1 / 100) * dc_value
