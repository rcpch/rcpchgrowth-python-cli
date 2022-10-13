"""
RCPCHGrowth Command Line Tool
"""


# standard imports
from datetime import date

# third party imports
import click
import pyfiglet
from scipy import stats

# RCPCH imports
from rcpchgrowth import date_calculations
from rcpchgrowth.global_functions import centile, measurement_from_sds, sds_for_measurement as sfm, mid_parental_height


@click.group()
def methods():
    """
    Performs calculations relating to the growth of infants, children and young people using the UK-WHO, 
    Down and Turner references. Developed by the RCPCH.
    """
    pass


@click.command()
@click.argument('birth_date', type=click.DateTime(formats=['%Y-%m-%d']),
                default=str(date.today()))
@click.argument('observation_date', type=click.DateTime(formats=['%Y-%m-%d']),
                default=str(date.today()))
@click.argument('gestation_weeks', type=click.INT, default=40, required=False)
@click.argument('gestation_days', type=click.INT, default=0, required=False)
@click.option('--adjustment', '-a', is_flag=True, default=False, help="Include if adjusting for gestational age.")
def age_calculation(birth_date, observation_date, gestation_weeks, gestation_days, adjustment):
    """
    Calculates decimal age, either chronological or corrected for gestation if the adjustment flag is true.\n
    Essential parameters are birth_date [format YY-M-DD], 
    observation_date [format YY-M-DD],
    Optional parameters are gestation_weeks (defaults to 40), 
    gestation_days (defaults to 0)\n
    If correction is required, supply the gestation and the --adjustment flag
    """
    click.echo("Calculates decimal age, either chronological or corrected for gestation if the adjustment flag is true. Params: birth_date, observation_date, gestation_weeks, gestation_days")
    decimal_age = 0
    calendar_age = ""
    if adjustment:
        decimal_age = date_calculations.corrected_decimal_age(
            birth_date=birth_date,
            observation_date=observation_date,
            gestation_weeks=gestation_weeks,
            gestation_days=gestation_days)
        corrected_birth_date = date_calculations.estimated_date_delivery(
            birth_date=birth_date,
            gestation_weeks=gestation_weeks,
            gestation_days=gestation_days)
        calendar_age = date_calculations.chronological_calendar_age(
            birth_date=corrected_birth_date,
            observation_date=observation_date)
        click.echo(f"Adjusted: {decimal_age} y,\n{calendar_age}")
    else:
        decimal_age = date_calculations.chronological_decimal_age(
            birth_date=birth_date,
            observation_date=observation_date)
        calendar_age = date_calculations.chronological_calendar_age(
            birth_date=birth_date,
            observation_date=observation_date)
        click.echo(f"Unadjusted: {decimal_age} y,\n{calendar_age}")


@click.command()
@click.argument('decimal_age', type=click.FLOAT)
@click.argument('measurement_method', default="height", type=click.Choice(['height', 'weight', 'bmi', 'ofc']))
@click.argument('sex', default="male", type=click.Choice(['male', 'female'], case_sensitive=True))
@click.argument('observation_value', type=click.FLOAT)
@click.option('--reference', '-r', default="uk-who", show_default=True, type=click.Choice(["uk-who", "trisomy-21", "turners-syndrome"], case_sensitive=True), nargs=1)
def sds_for_measurement(decimal_age, measurement_method, observation_value, sex, reference):
    """
    Returns an SDS for a given measurement\n
    Required parameters are: 
    decimal age as a float value, 
    measurement method as one of 'height', 'weight', 'bmi', 'ofc' (head circumference).
    sex as one of 'male' or 'female' (default 'male'),
    observation_value as a float value.
    The reference is optional - default is UK-WHO\n
    To change the reference pass --reference with one of "uk-who", "trisomy-21", "turners-syndrome"
    """

    result = sfm(
        reference=reference,
        age=decimal_age,
        measurement_method=measurement_method,
        observation_value=observation_value,
        sex=sex
    )

    cent = centile(result)
    click.echo(f"Reference: {reference_to_string(reference)}")
    click.echo(f"SDS: {result}\nCentile: {round(cent,1)} %\n")


@click.command()
@click.argument('decimal_age', type=click.FLOAT)
@click.argument('measurement_method', default="height", type=click.Choice(['height', 'weight', 'bmi', 'ofc']))
@click.argument('sex', default="male", type=click.Choice(['male', 'female'], case_sensitive=True))
@click.argument('centile', type=click.FLOAT)
@click.option('--reference', '-r', default="uk-who", show_default=True, type=click.Choice(["uk-who", "trisomy-21", "turners-syndrome"], case_sensitive=True))
def measurement_for_centile(decimal_age, sex, measurement_method, centile, reference):
    """
    Returns a measurement for a given centile\n
    Parameters include decimal age as a float, 
    measurement method as one of 'height', 'weight', 'bmi', 'ofc' (head circumference),
    sex as one of 'male' or 'female' (default 'male').
    centile as a float value,
    To change the reference pass --reference with one of "uk-who", "trisomy-21", "turners-syndrome"
    """

    # convert centile to SDS
    sds = stats.norm.ppf(centile / 100)

    # get measurement from SDS based on reference selected
    result = measurement_from_sds(
        reference=reference,
        requested_sds=sds,
        measurement_method=measurement_method,
        sex=sex,
        age=decimal_age
    )

    suffix = "cm"
    if measurement_method == "weight":
        suffix = "kg"
    elif measurement_method == "bmi":
        suffix = "kg/m2"
    click.echo(f"Reference: {reference_to_string(reference)}")
    click.echo(
        f"SDS {round(sds, 3)}\nCentile: {centile} %\n{measurement_method}: {result} {suffix}")


@click.command()
@click.argument('decimal_age', type=click.FLOAT)
@click.argument('measurement_method', default="height", type=click.Choice(['height', 'weight', 'bmi', 'ofc']))
@click.argument('sex', default="male", type=click.Choice(['male', 'female'], case_sensitive=True))
@click.argument('sds', type=click.FLOAT)
@click.option('--reference', '-r', default="uk-who", show_default=True, type=click.Choice(["uk-who", "trisomy-21", "turners-syndrome"], case_sensitive=True))
def measurement_for_sds(reference, decimal_age, sex, measurement_method, sds):
    """
    Returns a measurement for a given SDS\n
    Parameters include decimal age as a float, 
    measurement method as one of 'height', 'weight', 'bmi', 'ofc' (head circumference),
    sex as one of 'male' or 'female' (default 'male').
    sds as a float value,
    To change the reference pass --reference with one of "uk-who", "trisomy-21", "turners-syndrome"
    """
    result = measurement_from_sds(
        reference=reference,
        requested_sds=sds,
        measurement_method=measurement_method,
        sex=sex,
        age=decimal_age
    )
    cent = centile(sds)
    suffix = "cm"
    if measurement_method == "weight":
        suffix = "kg"
    elif measurement_method == "bmi":
        suffix = "kg/m2"
    click.echo(f"Reference: {reference_to_string(reference)}")
    click.echo(
        f"SDS {sds}\nCentile: {round(cent,3)} %\n{measurement_method}: {result} {suffix}")


@click.command()
@click.argument("maternal_height", type=click.FLOAT)
@click.argument("paternal_height", type=click.FLOAT)
@click.argument('sex', default="male", type=click.Choice(['male', 'female'], case_sensitive=True))
def midparental_height(maternal_height: float, paternal_height: float, sex: str):
    """
    Returns a midparental height
    Parameters include paternal_height in cm, maternal_height in cm and sex as one of 'male' or 'female' (default 'male').
    """
    result = None
    try:
        result = mid_parental_height(
            height_paternal=paternal_height,
            height_maternal=maternal_height,
            sex=sex
        )
    except Exception as e:
        return f"Error: {e}"
    click.echo(f"Midparental height: {round(result, 2)} cm")


fig = pyfiglet.Figlet(font="standard")
click.echo(fig.renderText("RCPCHGrowth"))
methods.add_command(age_calculation)
methods.add_command(sds_for_measurement)
methods.add_command(measurement_for_centile)
methods.add_command(measurement_for_sds)
methods.add_command(midparental_height)


if __name__ == '__main__':
    methods()


def reference_to_string(reference: str):
    if reference == "uk-who":
        return "UK-WHO"
    elif reference == "turners-syndrome":
        return "Turner's Syndrome"
    elif reference == "trisomy-21":
        return "Trisomy 21/Down's Syndrome"
    else:
        return "Reference error."
