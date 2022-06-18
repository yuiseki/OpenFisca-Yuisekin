"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Person, a Household…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_yuisekin.entities import Household


class total_benefits(Variable):
    value_type = float
    entity = Household
    definition_period = MONTH
    label = "Sum of the benefits perceived by a household"
    reference = "https://stats.gov.example/benefits"

    def formula(household, period, _parameters):
        """Total benefits."""
        ベーシックインカム_i = household.members("ベーシックインカム", period)  # Calculates the value of ベーシックインカム for each member of the household

        return (
            + household.sum(ベーシックインカム_i)  # Sum the household members ベーシックインカムs
            + household("住宅手当", period)
            )


class total_税金(Variable):
    value_type = float
    entity = Household
    definition_period = MONTH
    label = "Sum of the 税金 paid by a household"
    reference = "https://stats.gov.example/税金"

    def formula(household, period, _parameters):
        """Total 税金."""
        所得税_i = household.members("所得税", period)
        social_security_contribution_i = household.members("social_security_contribution", period)

        return (
            + household.sum(所得税_i)
            + household.sum(social_security_contribution_i)
            + household("housing_tax", period.this_year) / 12
            )
