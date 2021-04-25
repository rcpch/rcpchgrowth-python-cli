import click
from datetime import datetime
from rcpchgrowth import date_calculations
from rcpchgrowth import centile_bands
from rcpchgrowth.centile_bands import centile_band_for_centile
from rcpchgrowth.global_functions import centile, measurement_from_sds, sds_for_measurement

@click.group()
def methods():
    pass

@click.command()
@click.argument('birth_date')
@click.argument('observation_date')
@click.argument('gestation_weeks')
@click.argument('gestation_days')
@click.option('--adjustment', '-a')
def age_calculation(birth_date: datetime, observation_date: datetime, gestation_weeks=40, gestation_days=0, adjustment=False):
    decimal_age=0
    calendar_age=""
    if adjustment:
        decimal_age=date_calculations.corrected_decimal_age(
            birth_date=birth_date,
            observation_date=observation_date,
            gestation_weeks=gestation_weeks,
            gestation_days=gestation_days)
        calendar_age=date_calculations.chronological_calendar_age(
            birth_date=birth_date, 
            observation_date=observation_date)
    else:
        decimal_age=date_calculations.chronological_decimal_age(
            birth_date=birth_date,
            observation_date=observation_date
        )
        calendar_age=date_calculations.chronological_calendar_age(
            birth_date=birth_date, 
            observation_date=observation_date)
    click.echo(f"{decimal_age} y, \n {calendar_age}")

@click.command()
@click.argument('reference')
@click.argument('decimal_age')
@click.argument('measurement_method')
@click.argument('observation_value')
@click.argument('sex')
def sds(reference: str, decimal_age: float, measurement_method: str, observation_value: float, sex: str):
    result = sds_for_measurement(
        reference=reference,
        age=decimal_age,
        measurement_method=measurement_method,
        observation_value=observation_value,
        sex=sex
    )
    cent = centile(result)
    click.echo(f"SDS: {result}\n Centile: {cent}\n ")

@click.command()
@click.argument('reference')
@click.argument('decimal_age')
@click.argument('sex')
@click.argument('measurement_method')
@click.argument('sds')
def measurement(reference: str, decimal_age: float, sex:str, measurement_method: str, sds: float):
    result = measurement_from_sds(
        reference, 
        requested_sds=sds,
        measurement_method=measurement_method,
        sex=sex,
        age=decimal_age
    )
    suffix="cm"
    if measurement_method=="weight":
        suffix="kg"
    elif measurement_method=="bmi":
        suffix="kg/m2"
    click.echo(f"SDS {sds}\n {measurement_method}: {result} {suffix}")


methods.add_command(age_calculation)
methods.add_command(sds)
methods.add_command(measurement)

if __name__ == '__main__':
    methods()
