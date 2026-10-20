import unittest
from unittest.mock import patch

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from staticPlots import staticPlots


class DailyRidershipComparisonTests(unittest.TestCase):
    def frame(self, rows):
        return pd.DataFrame(rows, columns=[
            "direction", "stopId", "stopName", "stopOrderNum", "timeOfDay",
            "dailyAlightings", "dailyBoardings",
        ])

    def plot(self, first, second):
        with (
            patch.object(staticPlots.pd, "read_csv", side_effect=[first, second]),
            patch.object(staticPlots.os, "makedirs"),
            patch("matplotlib.figure.Figure.savefig", autospec=True) as save,
        ):
            output = staticPlots.plot_daily_ridership_comparison_from_csv(
                "first.csv", "second.csv", "ct", "701", "2310", "2410"
            )
        self.assertEqual(
            output, "../STR/ct/701/2310_vs_2410/DailyRidership.png"
        )
        self.assertEqual(save.call_args.args[1], output)
        fig = save.call_args.args[0]
        self.assertFalse(plt.fignum_exists(fig.number))
        return fig

    def test_adjacent_faded_stacks_and_shared_limits(self):
        first = self.frame([
            ["I", 1, "Stop", 0, "AM", 2, 3],
            ["I", 1, "Stop", 0, "MID", 4, 5],
        ])
        second = self.frame([["I", 1, "Stop", 0, "AM", 10, 20]])
        fig = self.plot(first, second)
        inbound, outbound = fig.axes
        bars = inbound.patches
        self.assertEqual([bar.get_width() for bar in bars], [-2, 3, -4, 5, -10, 20])
        self.assertEqual([bar.get_x() for bar in bars], [0, 0, -2, 3, 0, 0])
        self.assertEqual([bar.get_alpha() for bar in bars], [0.5] * 4 + [1.0] * 2)
        self.assertAlmostEqual(bars[0].get_y() - bars[-1].get_y(), 0.3)
        self.assertEqual(bars[0].get_facecolor()[:3], bars[-1].get_facecolor()[:3])
        self.assertEqual(inbound.get_xlim(), outbound.get_xlim())
        self.assertEqual(inbound.get_xlim(), (-11, 22))
        legend = [text.get_text() for text in inbound.get_legend().get_texts()]
        self.assertEqual(len(legend), 10)
        self.assertIn("October 2023 5am-9am (AM)", legend)
        self.assertIn("October 2024 5am-9am (AM)", legend)
        self.assertIn("Swift Blue Line", fig._suptitle.get_text())

    def test_unequal_stop_counts_align_by_id(self):
        first = self.frame([
            ["I", 1, "Old name", 0, "AM", 1, 2],
            ["I", 2, "Removed", 1, "AM", 3, 4],
            ["I", 4, "Also removed", 2, "AM", 5, 6],
            ["O", 1, "Outbound old", 2, "AM", 5, 6],
        ])
        second = self.frame([
            ["I", 1, "New name", 3, "AM", 7, 8],
            ["I", 3, "Added", 0, "AM", 9, 10],
            ["O", 1, "Outbound new", 0, "AM", 11, 12],
            ["O", 4, "Outbound added", 1, "AM", 13, 14],
        ])
        inbound, outbound = self.plot(first, second).axes
        self.assertEqual(
            [tick.get_text() for tick in inbound.get_yticklabels()],
            ["New name", "Also removed", "Removed", "Added"],
        )
        self.assertEqual(
            [tick.get_text() for tick in outbound.get_yticklabels()],
            ["Outbound new", "Outbound added"],
        )
        first_bar, second_bar = inbound.patches[:4:2]
        self.assertAlmostEqual(first_bar.get_y() + first_bar.get_height() / 2, 0.15)
        self.assertAlmostEqual(second_bar.get_y() + second_bar.get_height() / 2, -0.15)
        self.assertEqual(len(inbound.patches), 10)

    def test_equal_stop_counts_align_changed_ids_by_position(self):
        for direction in ["I", "O"]:
            with self.subTest(direction=direction):
                first = self.frame([
                    [direction, 0, "A", 0, "AM", 1, 10],
                    [direction, 1, "B", 1, "AM", 2, 20],
                    [direction, 2, "C", 2, "AM", 3, 30],
                    [direction, 2, "C", 2, "MID", 4, 40],
                    [direction, 3, "D", 3, "AM", 5, 50],
                ])
                second = self.frame([
                    [direction, 0, "A", 10, "AM", 6, 60],
                    [direction, 1, "B", 20, "AM", 7, 70],
                    [direction, 5, "E", 30, "AM", 8, 80],
                    [direction, 3, "D", 40, "AM", 9, 90],
                ]).iloc[::-1]
                ax = self.plot(first, second).axes[0 if direction == "I" else 1]
                expected = ["A", "B", "E", "D"]
                if direction == "I":
                    expected.reverse()
                self.assertEqual(
                    [tick.get_text() for tick in ax.get_yticklabels()], expected
                )
                position = expected.index("E")
                bars = [
                    bar for bar in ax.patches
                    if abs(bar.get_y() + bar.get_height() / 2 - position) < 0.2
                ]
                self.assertEqual(
                    [bar.get_width() for bar in bars], [-3, 30, -4, 40, -8, 80]
                )
                self.assertEqual([bar.get_alpha() for bar in bars], [0.5] * 4 + [1] * 2)

    def test_equal_stop_counts_handle_swapped_ids_without_merging_data(self):
        first = self.frame([
            ["O", 1, "First old", 0, "AM", 1, 10],
            ["O", 2, "Second old", 1, "AM", 2, 20],
        ])
        second = self.frame([
            ["O", 2, "First new", 0, "AM", 3, 30],
            ["O", 1, "Second new", 1, "AM", 4, 40],
        ])
        ax = self.plot(first, second).axes[1]
        self.assertEqual(
            [tick.get_text() for tick in ax.get_yticklabels()],
            ["First new", "Second new"],
        )
        self.assertEqual(
            [bar.get_width() for bar in ax.patches],
            [-1, 10, -3, 30, -2, 20, -4, 40],
        )

    def test_duplicate_time_rows_are_summed(self):
        frame = self.frame([
            ["I", 1, "Stop", 0, "AM", 2, 3],
            ["I", 1, "Stop", 0, "AM", 4, 5],
        ])
        bars = self.plot(frame, frame).axes[0].patches
        self.assertEqual([bar.get_width() for bar in bars], [-6, 8, -6, 8])

    def test_zero_values_keep_non_degenerate_limits(self):
        frame = self.frame([["O", 1, "Stop", 0, "PM", 0, 0]])
        fig = self.plot(frame, frame)
        self.assertEqual(fig.axes[0].get_xlim(), (-1, 1))
        self.assertEqual(fig.axes[1].get_xlim(), (-1, 1))

    def test_empty_input_is_rejected(self):
        empty = self.frame([])
        populated = self.frame([["I", 1, "Stop", 0, "AM", 1, 2]])
        for frames in ([empty, populated], [populated, empty]):
            with patch.object(staticPlots.pd, "read_csv", side_effect=frames):
                with self.assertRaisesRegex(ValueError, "No data found"):
                    staticPlots.plot_daily_ridership_comparison_from_csv(
                        "first.csv", "second.csv", "ct", "701", "2310", "2410"
                    )


if __name__ == "__main__":
    unittest.main()
