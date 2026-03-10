import unittest

from solution import recommend_appointment_slots


class AppointmentSlotRecommenderTests(unittest.TestCase):
    # Validates C1, C6, C7, C8 (AC1)
    def test_no_busy_times_returns_full_working_window(self):
        result = recommend_appointment_slots(("09:00", "17:00"), [], 30)
        self.assertEqual(result, [("09:00", "17:00")])

    # Validates C2, C6 (AC2)
    def test_busy_interval_is_excluded(self):
        result = recommend_appointment_slots(
            ("09:00", "17:00"),
            [("10:00", "11:00")],
            30,
        )
        self.assertEqual(result, [("09:00", "10:00"), ("11:00", "17:00")])

    # Validates C4, C6 (AC3)
    def test_all_returned_slots_meet_required_duration(self):
        result = recommend_appointment_slots(
            ("09:00", "12:00"),
            [("09:30", "10:00"), ("10:45", "11:30")],
            45,
        )
        self.assertEqual(result, [("10:00", "10:45")])

    # Validates C5, C6 (AC4) - edge case: buffer removes otherwise valid slot
    def test_buffer_time_removes_otherwise_valid_slot(self):
        result = recommend_appointment_slots(
            ("09:00", "12:00"),
            [("10:00", "11:00")],
            31,
            buffer_time=30,
        )
        self.assertEqual(result, [])

    # Validates C7 (AC5) - edge case: candidate window too small
    def test_candidate_window_restricts_results_and_can_be_too_small(self):
        result = recommend_appointment_slots(
            ("09:00", "17:00"),
            [("13:10", "13:20")],
            25,
            candidate_window=("13:00", "13:25"),
        )
        self.assertEqual(result, [])

    # Validates C8 and normalization behavior for overlapping/unsorted busy intervals
    def test_overlapping_and_unsorted_busy_intervals_are_normalized(self):
        result = recommend_appointment_slots(
            ("09:00", "17:00"),
            [("14:00", "15:00"), ("10:00", "12:00"), ("11:30", "13:00")],
            30,
        )
        self.assertEqual(result, [("09:00", "10:00"), ("13:00", "14:00"), ("15:00", "17:00")])

    # Edge case: meeting duration longer than any available gap
    def test_duration_longer_than_any_gap_returns_empty(self):
        result = recommend_appointment_slots(
            ("09:00", "12:00"),
            [("09:30", "10:30"), ("11:00", "11:30")],
            45,
        )
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
