"""Appointment Slot Recommender for EECS 4312 Lab 8 Task A."""

from __future__ import annotations

from typing import List, Optional, Tuple


TimeInterval = Tuple[str, str]
MinutesInterval = Tuple[int, int]


def _to_minutes(time_str: str) -> int:
    """Convert HH:MM string to minutes from midnight."""
    hour_str, minute_str = time_str.split(":")
    hour = int(hour_str)
    minute = int(minute_str)
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        raise ValueError(f"Invalid time format: {time_str}")
    return hour * 60 + minute


def _to_time_str(total_minutes: int) -> str:
    """Convert minutes from midnight to HH:MM string."""
    hour = total_minutes // 60
    minute = total_minutes % 60
    return f"{hour:02d}:{minute:02d}"


def _validate_interval(interval: TimeInterval, name: str) -> MinutesInterval:
    start, end = interval
    start_m = _to_minutes(start)
    end_m = _to_minutes(end)
    if start_m >= end_m:
        raise ValueError(f"{name} start time must be before end time")
    return start_m, end_m


def _merge_intervals(intervals: List[MinutesInterval]) -> List[MinutesInterval]:
    """Merge overlapping or touching intervals."""
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda item: item[0])
    merged: List[MinutesInterval] = [ordered[0]]
    for start, end in ordered[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def recommend_appointment_slots(
    working_hours: TimeInterval,
    busy_intervals: List[TimeInterval],
    meeting_duration: int,
    buffer_time: int = 0,
    candidate_window: Optional[TimeInterval] = None,
) -> List[TimeInterval]:
    """
    Recommend available appointment slots as free intervals.

    Each returned interval is at least meeting_duration minutes long and
    does not overlap busy intervals (including optional buffer).
    """
    # C1
    work_start, work_end = _validate_interval(working_hours, "Working hours")

    # C4
    if meeting_duration <= 0:
        raise ValueError("Meeting duration must be greater than zero")

    # C5
    if buffer_time < 0:
        raise ValueError("Buffer time must be zero or positive")

    window_start, window_end = work_start, work_end
    if candidate_window is not None:
        cand_start, cand_end = _validate_interval(candidate_window, "Candidate window")
        window_start = max(window_start, cand_start)
        window_end = min(window_end, cand_end)

    if window_start >= window_end:
        return []

    expanded_busy: List[MinutesInterval] = []
    for index, interval in enumerate(busy_intervals):
        # C2
        busy_start, busy_end = _validate_interval(interval, f"Busy interval {index}")
        start = max(window_start, busy_start - buffer_time)
        end = min(window_end, busy_end + buffer_time)
        if start < end:
            expanded_busy.append((start, end))

    normalized_busy = _merge_intervals(expanded_busy)

    free_slots: List[MinutesInterval] = []
    cursor = window_start
    for busy_start, busy_end in normalized_busy:
        if cursor < busy_start and busy_start - cursor >= meeting_duration:
            free_slots.append((cursor, busy_start))
        cursor = max(cursor, busy_end)

    if window_end - cursor >= meeting_duration:
        free_slots.append((cursor, window_end))

    # C8: already chronological because of sorted merged intervals and forward cursor.
    return [(_to_time_str(start), _to_time_str(end)) for start, end in free_slots]