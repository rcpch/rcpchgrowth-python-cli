import click
from datetime import datetime
from click.utils import echo
from rcpchgrowth import date_calculations
from rcpchgrowth import centile_bands
from rcpchgrowth.centile_bands import centile_band_for_centile
from rcpchgrowth.global_functions import centile, measurement_from_sds, sds_for_measurement
import pyfiglet

@click.group()
def methods():
    """
    Performs calculations relating to the growth of infants, children and young people using the UK-WHO, 
    Down and Turner references. Developed by the RCPCH.
    """
    pass

@click.command()
@click.argument('birth_date')
@click.argument('observation_date')
@click.argument('gestation_weeks')
@click.argument('gestation_days')
@click.option('--adjustment', '-a', help="Include if adjusting for gestational age.")
def age_calculation(birth_date: datetime, observation_date: datetime, gestation_weeks=40, gestation_days=0, adjustment=False):
    """
    Calculates decimal age, either chronological or corrected for gestation if the adjustment flag is true.
    birth_date, observation_date, gestation_weeks, gestation_days
    """
    click.echo("Calculates decimal age, either chronological or corrected for gestation if the adjustment flag is true. Params: birth_date, observation_date, gestation_weeks, gestation_days")
    decimal_age=0
    calendar_age=""
    if adjustment:
        decimal_age=date_calculations.corrected_decimal_age(
            birth_date=datetime.strptime(birth_date, "%Y-%m-%d").date(),
            observation_date=datetime.strptime(observation_date,"%Y-%m-%d").date(),
            gestation_weeks=gestation_weeks,
            gestation_days=gestation_days)
        calendar_age=date_calculations.chronological_calendar_age(
            birth_date=datetime.strptime(birth_date, "%Y-%m-%d").date(),
            observation_date=datetime.strptime(observation_date,"%Y-%m-%d").date())
    else:
        decimal_age=date_calculations.chronological_decimal_age(
            birth_date=datetime.strptime(birth_date, "%Y-%m-%d").date(),
            observation_date=datetime.strptime(observation_date,"%Y-%m-%d").date(),
        )
        calendar_age=date_calculations.chronological_calendar_age(
            birth_date=datetime.strptime(birth_date, "%Y-%m-%d").date(),
            observation_date=datetime.strptime(observation_date,"%Y-%m-%d").date())
    click.echo(f"{decimal_age} y,\n {calendar_age}")

@click.command()
@click.option('--reference', '-r', default="uk-who", show_default=True, type=click.Choice(["uk-who", "trisomy-21", "turners-syndrome"], case_sensitive=True))
@click.argument('decimal_age', type=click.FLOAT)
@click.option('--measurement-method', '-m', default="height", show_default=True, type=click.Choice(['height', 'weight', 'bmi', 'ofc']))
@click.option('--sex', '-s', default="male", show_default=True, type=click.Choice(['male', 'female'], case_sensitive=True))
@click.argument('observation_value', type=click.FLOAT)
def sds(reference: str, decimal_age: float, measurement_method: str, observation_value: float, sex: str):
    """
    Returns a z score
    """
    result = sds_for_measurement(
        reference=reference,
        age=decimal_age,
        measurement_method=measurement_method,
        observation_value=observation_value,
        sex=sex
    )
    cent = centile(result)
    click.echo(f"SDS: {result}\nCentile: {round(cent,1)} %\n")

@click.command()
@click.option('--reference', '-r', default="uk-who", show_default=True, type=click.Choice(["uk-who", "trisomy-21", "turners-syndrome"], case_sensitive=True))
@click.argument('decimal_age', type=click.FLOAT)
@click.option('--measurement-method', '-m', default="height", show_default=True, type=click.Choice(['height', 'weight', 'bmi', 'ofc']))
@click.option('--sex', '-s', default="male", show_default=True, type=click.Choice(['male', 'female'], case_sensitive=True))
@click.argument('sds', type=click.FLOAT)
def measurement(reference: str, decimal_age: float, sex: str, measurement_method: str, sds: float):
    """
    Returns a measurement for a give z score
    """
    result = measurement_from_sds(
        reference=reference, 
        requested_sds=sds,
        measurement_method=measurement_method,
        sex=sex,
        age=decimal_age
    )
    cent = centile(sds)
    suffix="cm"
    if measurement_method=="weight":
        suffix="kg"
    elif measurement_method=="bmi":
        suffix="kg/m2"
    click.echo(f"SDS {sds}\nCentile: {round(cent,3)} %\n{measurement_method}: {result} {suffix}")

fig = pyfiglet.Figlet(font="standard")
click.echo(fig.renderText("RCPCHGrowth"))
methods.add_command(age_calculation)
methods.add_command(sds)
methods.add_command(measurement)

if __name__ == '__main__':
    methods()
