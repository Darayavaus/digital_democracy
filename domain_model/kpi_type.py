

from enum import Enum


class KpiType(str, Enum):
    """
    Various types of KPIs
    """
    IMPACT = "Impact"
    COHERENCE = "Coherence"
    ALIGNMENT = "Alignment"
    PROGRESS = "Progress"
    INFO_AVAILABILITY = "Info availability"
    MEDIA_COVERAGE = "Media coverage"
