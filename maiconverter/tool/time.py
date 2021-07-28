import math
from typing import List, Tuple


def _check_bpms(bpms: List[Tuple[float, float]]):
    if len(bpms) == 0:
        raise ValueError("No BPMs given.")
    if not any([x for x in bpms if 0.0 <= x[0] <= 1.0]):
        raise ValueError("No starting BPM defined.")


def measure_to_second(measure: float, bpms: List[Tuple[float, float]]) -> float:
    if measure <= 1.0:
        return 0.0

    _check_bpms(bpms)
    bpms.sort(key=lambda x: x[0])

    previous_measure = 1.0
    previous_bpm = bpms[0][1]
    previous_time = 0.0
    for current_measure, current_bpm in bpms:
        gap_measure = current_measure - previous_measure
        gap_time = 60 * 4 * gap_measure / previous_bpm

        current_time = previous_time + gap_time
        if math.isclose(current_measure, measure, abs_tol=0.0005):
            return current_time
        if current_measure > measure:
            break

        previous_measure = current_measure
        previous_bpm = current_bpm
        previous_time = current_time

    gap_measure = measure - previous_measure
    gap_time = 60 * 4 * gap_measure / previous_bpm

    return previous_time + gap_time


def second_to_measure(seconds: float, bpms: List[Tuple[float, float]]) -> float:
    if seconds <= 0.0:
        return 1.0

    _check_bpms(bpms)
    bpms.sort(key=lambda x: x[0])

    previous_measure = 1.0
    previous_time = 0.0
    previous_bpm = bpms[0][1]
    for current_measure, current_bpm in bpms:
        gap_measure = current_measure - previous_measure
        # Time (in seconds) = 60 seconds per minute * measure * beats per measure / BPM
        gap_time = 60 * gap_measure * 4 / previous_bpm
        current_time = previous_time + gap_time

        if math.isclose(current_time, seconds, abs_tol=0.0005):
            return current_measure
        if current_time > seconds:
            break

        previous_measure = current_measure
        previous_time = current_time
        previous_bpm = current_bpm

    gap_time = seconds - previous_time
    gap_measure = gap_time * previous_bpm / (60 * 4)

    return previous_measure + gap_measure


def quantise(measure: float, grid: int) -> float:
    if grid <= 0:
        raise ValueError(f"Quantisation is not positive: {grid}")

    return round(grid * measure) / grid
