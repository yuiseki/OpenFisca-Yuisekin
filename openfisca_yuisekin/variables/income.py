"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Person, a Household…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.holders import set_input_divide_by_period
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_yuisekin.entities import Person


# This variable is a pure input: it doesn't have a formula
class 所得(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    set_input = set_input_divide_by_period  # Optional attribute. Allows user to declare a 所得 for a year. OpenFisca will spread the yearly amount over the months contained in the year.
    label = "所得"
    reference = "https://law.gov.example/所得"  # Always use the most official source


class 可処分所得(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    label = "Actual amount available to the person at the end of the month"
    reference = "https://stats.gov.example/可処分所得"  # Some variables represent quantities used in economic models, and not defined by law. Always give the source of your definitions.

    def formula(person, period, _parameters):
        """Disposable income."""
        return (
            + person("所得", period)
            + person("ベーシックインカム", period)
            - person("所得税", period)
            - person("social_security_contribution", period)
            )
