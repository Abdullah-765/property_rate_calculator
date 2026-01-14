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

#calculates the advance tax for all the categories
def calculate_advance_tax_all(value):
    def calculate_for_filer():
        if value <= 50_000_000:
            return (1.5 / 100) * value, 1.5
        elif value <= 100_000_000:
            return (2 / 100) * value, 2
        return (2.5 / 100) * value, 2.5
    def calculate_for_non_filer():
        if value <= 50_000_000:
            return (10.5 / 100) * value, 10.5
        elif value <= 100_000_000:
            return (14.5 / 100) * value, 14.5
        return (18.5 / 100) * value, 18.5
    def calculate_for_late_filer():
        if value <= 50_000_000:
            return (4.5 / 100) * value, 4.5
        elif value <= 100_000_000:
            return (5.5 / 100) * value, 5.5
        return (6.5 / 100) * value, 6.5
    
    calculate_advance_tax_filer_val, calculate_advance_tax_filer_percentage = calculate_for_filer()
    calculate_advance_tax_non_filer_val, calculate_advance_tax_non_filer_percentage = calculate_for_non_filer()
    calculate_advance_tax_late_filer_val, calculate_advance_tax_late_filer_percentage = calculate_for_late_filer()

    return [
        calculate_advance_tax_filer_val,
        calculate_advance_tax_filer_percentage,
        calculate_advance_tax_non_filer_val,
        calculate_advance_tax_non_filer_percentage,
        calculate_advance_tax_late_filer_val,
        calculate_advance_tax_late_filer_percentage
    ]

#calculates the advance tax for all the categories
def calculate_gain_tax_all(value):
    def calculate_for_filer():
        if value <= 50_000_000:
            return (4.5 / 100) * value, 4.5
        elif value <= 100_000_000:
            return (5 / 100) * value, 5
        return (5.5 / 100) * value, 5.5
    def calculate_for_non_filer():
        if value <= 50_000_000:
            return (11.5 / 100) * value, 11.5
        elif value <= 100_000_000:
            return (11.5 / 100) * value, 11.5
        return (11.5 / 100) * value, 11.5
    def calculate_for_late_filer():
        if value <= 50_000_000:
            return (7.5 / 100) * value, 7.5
        elif value <= 100_000_000:
            return (8.5 / 100) * value, 8.5
        return (9.5 / 100) * value, 9.5
    
    calculate_gain_tax_filer_val, calculate_gain_tax_filer_percentage = calculate_for_filer()
    calculate_gain_tax_non_filer_val, calculate_gain_tax_non_filer_percentage = calculate_for_non_filer()
    calculate_gain_tax_late_filer_val, calculate_gain_tax_late_filer_percentage = calculate_for_late_filer()

    return [
        calculate_gain_tax_filer_val,
        calculate_gain_tax_filer_percentage,
        calculate_gain_tax_non_filer_val,
        calculate_gain_tax_non_filer_percentage,
        calculate_gain_tax_late_filer_val,
        calculate_gain_tax_late_filer_percentage
    ]

def calculate_stamp_duty(value):
    return STAMP_DUTY_PERCENTAGE * value

def calculate_seller_7e(value):
    return SELLER_7E_PERCENTAGE * value


def calculate_town_tax(value):
    return (1 / 100) * value
