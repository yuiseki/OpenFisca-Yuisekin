"""
国民年金の実装
"""

from datetime import date
from datetime import datetime

from dateutil.relativedelta import relativedelta
from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import ETERNITY
from openfisca_core.variables import Variable
from openfisca_yuisekin.entities import 人物


class 身体障害者手帳最新交付年月日(Variable):
    value_type = date
    entity = 人物
    label = "人物の身体障害者手帳の最新交付年月日"
    definition_period = ETERNITY


class 国民年金被保険者パターン(Enum):
    __order__ = "無 第1号被保険者 第2号被保険者 第3号被保険者"
    無 = "無"
    第1号被保険者 = "第1号被保険者"
    第2号被保険者 = "第2号被保険者"
    第3号被保険者 = "第3号被保険者"


class 国民年金被保険者(Variable):
    value_type = Enum
    possible_values = 国民年金被保険者パターン
    default_value = 国民年金被保険者パターン.無
    entity = 人物
    definition_period = ETERNITY
    label = "人物の国民年金被保険者"

    def formula(対象人物, 対象期間, parameters):
      年齢 = 対象人物("年齢", 対象期間)
      開始年齢 = parameters(対象期間).福祉.第1号被保険者.開始年齢
      終了年齢 = parameters(対象期間).福祉.第1号被保険者.終了年齢
      条件 = (開始年齢 <= 年齢) * (年齢 < 終了年齢)
      return (条件 * 国民年金被保険者パターン.第1号被保険者)
