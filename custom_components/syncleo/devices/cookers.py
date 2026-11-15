"""Polaris multicookers on the Syncleo platform.

Verified against a real PMC-0528WIFI (mDNS devtype 48, firmware 2.17, protocol 2):
the device pushes current temperature, error, keep-warm and child-lock on connect and
echoes child-lock writes back immediately, so these entities are safe read/write.
Target temperature, cook timer and delay start are exposed as numbers over the same
commands; starting a program (mode/recipe) is intentionally not exposed yet — the
program codes have to be mapped first.
"""

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfTemperature, UnitOfTime

from ..const import (
    FEATURE_CHILD_LOCK,
    FEATURE_COOKER_CURRENT_TEMPERATURE,
    FEATURE_COOKER_DELAY_START,
    FEATURE_COOKER_TARGET_TEMPERATURE,
    FEATURE_ERROR,
    FEATURE_KEEP_WARM,
    FEATURE_TIMER,
    VENDOR_POLARIS,
)
from .profiles import CookerProfile, NumberConfig, SensorConfig

_COOKER_NUMBER_CONFIGS = {
    FEATURE_COOKER_TARGET_TEMPERATURE: NumberConfig(
        min_value=30,
        max_value=160,
        step=5,
        unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    FEATURE_TIMER: NumberConfig(
        min_value=1,
        max_value=720,
        step=1,
        unit_of_measurement=UnitOfTime.MINUTES,
    ),
    FEATURE_COOKER_DELAY_START: NumberConfig(
        min_value=0,
        max_value=1440,
        step=10,
        unit_of_measurement=UnitOfTime.MINUTES,
    ),
}


def _create_polaris_cooker(device_type: int, **kwargs) -> CookerProfile:
    params = {
        "vendor": VENDOR_POLARIS,
        "device_type": device_type,
        "binary_sensors": [FEATURE_ERROR],
        "sensors": {
            FEATURE_COOKER_CURRENT_TEMPERATURE: SensorConfig(
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                unit_of_measurement=UnitOfTemperature.CELSIUS,
            ),
        },
        "switches": [FEATURE_CHILD_LOCK, FEATURE_KEEP_WARM],
        "numbers": [
            FEATURE_COOKER_TARGET_TEMPERATURE,
            FEATURE_TIMER,
            FEATURE_COOKER_DELAY_START,
        ],
        "number_configs": dict(_COOKER_NUMBER_CONFIGS),
    } | kwargs
    return CookerProfile(**params)


PROFILES = [
    # Polaris PMC-0528WIFI (devtype 48) — verified on hardware
    _create_polaris_cooker(device_type=48),
    # same hardware family reported with another devtype in the Polaris app
    _create_polaris_cooker(device_type=268),
]
