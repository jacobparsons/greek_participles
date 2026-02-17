"""
Reveal Grid Game — Tkinter (multiple selectable grids via dropdown)

Features:
- Pick a grid set from a dropdown (OptionMenu)
- Grid + axis labels update immediately on selection
- Arbitrary dimensions inferred from the selected CELL_TEXTS
- Turn flow:
    1) Random covered cell is highlighted (still hidden)
    2) SPACE reveals its content
    3) ← Incorrect (re-covers) or → Correct (stays uncovered)
- Timer starts on first highlight; shows elapsed live; shows total at end
- Switching dropdown resets the game (fresh timer/score)

Run:
    python reveal_game.py
"""

import random
import time
import tkinter as tk
from tkinter import messagebox
from dataclasses import dataclass
from typing import List, Optional


# -----------------------------
# DATA: define as many grids as you want
# -----------------------------

@dataclass(frozen=True)
class GridSpec:
    name: str
    cell_texts: List[List[str]]
    col_labels: Optional[List[str]] = None
    row_labels: Optional[List[str]] = None


GRIDS = [

    # ---------------- PRESENT SYSTEM ----------------
    GridSpec(
        name="Present Act. Participle (Singular)",
        cell_texts=[
            ["λὐων", "λὐουσα", "λὐον"],
            ["λὐοντος", "λοὐσης", "λὐοντος"],
            ["λὐοντι", "λοὐση", "λὐοντι"],
            ["λὐοντα", "λὐουσαν", "λὐον"],
        ],
        col_labels=["Masculine", "Feminine", "Neuter"],
        row_labels=["Nominative", "Genitive", "Dative", "Accusative"],
    ),

    GridSpec(
        name="Present Middle/Passive Participle (Singular)",
        cell_texts=[
            ["λυόμενος", "λυομένη", "λυόμενον"],
            ["λυομένου", "λυομένης", "λυομένου"],
            ["λυομένῳ", "λυομένῃ", "λυομένῳ"],
            ["λυόμενον", "λυομένην", "λυόμενον"],
        ],
        col_labels=["Masculine", "Feminine", "Neuter"],
        row_labels=["Nominative", "Genitive", "Dative", "Accusative"],
    ),

    # ---------------- 1ST AORIST ----------------
    GridSpec(
        name="1st Aorist Act. Participle (Singular)",
        cell_texts=[
            ["λῡ́σᾱς", "λῡ́σᾱσα", "λῦσαν"],
            ["λῡ́σαντος", "λῡ́σᾱσης", "λῡ́σαντος"],
            ["λῡ́σαντι", "λῡ́σᾱσῃ", "λῡ́σαντι"],
            ["λῡ́σαντα", "λῡ́σᾱσαν", "λῦσαν"],
        ],
        col_labels=["Masculine", "Feminine", "Neuter"],
        row_labels=["Nominative", "Genitive", "Dative", "Accusative"],
    ),

    GridSpec(
        name="1st Aorist Middle Participle (Singular)",
        cell_texts=[
            ["λῡσάμενος", "λῡσαμένη", "λῡσάμενον"],
            ["λῡσαμένου", "λῡσαμένης", "λῡσαμένου"],
            ["λῡσαμένῳ", "λῡσαμένῃ", "λῡσαμένῳ"],
            ["λῡσάμενον", "λῡσαμένην", "λῡσάμενον"],
        ],
        col_labels=["Masculine", "Feminine", "Neuter"],
        row_labels=["Nominative", "Genitive", "Dative", "Accusative"],
    ),

    GridSpec(
        name="1st Aorist Passive Participle (Singular)",
        cell_texts=[
            ["λυθείς", "λυθεῖσα", "λυθέν"],
            ["λυθέντος", "λυθείσης", "λυθέντος"],
            ["λυθέντι", "λυθείσῃ", "λυθέντι"],
            ["λυθέντα", "λυθεῖσαν", "λυθέν"],
        ],
        col_labels=["Masculine", "Feminine", "Neuter"],
        row_labels=["Nominative", "Genitive", "Dative", "Accusative"],
    ),

    # ---------------- 2ND AORIST ----------------
    GridSpec(
        name="2nd Aorist Act. Participle (Singular) — λαβών type",
        cell_texts=[
            ["λαβών", "λαβοῦσα", "λαβόν"],
            ["λαβόντος", "λαβούσης", "λαβόντος"],
            ["λαβόντι", "λαβούσῃ", "λαβόντι"],
            ["λαβόντα", "λαβοῦσαν", "λαβόν"],
        ],
        col_labels=["Masculine", "Feminine", "Neuter"],
        row_labels=["Nominative", "Genitive", "Dative", "Accusative"],
    ),

    GridSpec(
        name="2nd Aorist Middle Participle (Singular) — γενόμενος type",
        cell_texts=[
            ["γενόμενος", "γενομένη", "γενόμενον"],
            ["γενομένου", "γενομένης", "γενομένου"],
            ["γενομένῳ", "γενομένῃ", "γενομένῳ"],
            ["γενόμενον", "γενομένην", "γενόμενον"],
        ],
        col_labels=["Masculine", "Feminine", "Neuter"],
        row_labels=["Nominative", "Genitive", "Dative", "Accusative"],
    ),

    GridSpec(
        name="2nd Aorist Passive Participle (Singular)",
        cell_texts=[
            ["γραφείς", "γραφεῖσα", "γραφέν"],
            ["γραφέντος", "γραφείσης", "γραφέντος"],
            ["γραφέντι", "γραφείσῃ", "γραφέντι"],
            ["γραφέντα", "γραφεῖσαν", "γραφέν"],
        ],
        col_labels=["Masculine", "Feminine", "Neuter"],
        row_labels=["Nominative", "Genitive", "Dative", "Accusative"],
    ),

    # ---------------- PERFECT ----------------
    GridSpec(
        name="Perfect Act. Participle (Singular)",
        cell_texts=[
            ["λελυκώς", "λελυκυῖα", "λελυκός"],
            ["λελυκότος", "λελυκυίας", "λελυκότος"],
            ["λελυκότι", "λελυκυίᾳ", "λελυκότι"],
            ["λελυκότα", "λελυκυῖαν", "λελυκός"],
        ],
        col_labels=["Masculine", "Feminine", "Neuter"],
        row_labels=["Nominative", "Genitive", "Dative", "Accusative"],
    ),

    GridSpec(
        name="Perfect Middle/Passive Participle (Singular)",
        cell_texts=[
            ["λελυμένος", "λελυμένη", "λελυμένον"],
            ["λελυμένου", "λελυμένης", "λελυμένου"],
            ["λελυμένῳ", "λελυμένῃ", "λελυμένῳ"],
            ["λελυμένον", "λελυμένην", "λελυμένον"],
        ],
        col_labels=["Masculine", "Feminine", "Neuter"],
        row_labels=["Nominative", "Genitive", "Dative", "Accusative"],
    ),
    
    # ---------------- FUTURE ----------------

    GridSpec(
        name="Future Active Participle (Singular)",
        cell_texts=[
            ["λύσων", "λύσουσα", "λύσον"],
            ["λύσοντος", "λυσούσης", "λύσοντος"],
            ["λύσοντι", "λυσούσῃ", "λύσοντι"],
            ["λύσοντα", "λύσουσαν", "λύσον"],
        ],
        col_labels=["Masculine", "Feminine", "Neuter"],
        row_labels=["Nominative", "Genitive", "Dative", "Accusative"],
    ),
    
    GridSpec(
        name="Future Middle Participle (Singular)",
        cell_texts=[
            ["λυσόμενος", "λυσομένη", "λυσόμενον"],
            ["λυσομένου", "λυσομένης", "λυσομένου"],
            ["λυσομένῳ", "λυσομένῃ", "λυσομένῳ"],
            ["λυσόμενον", "λυσομένην", "λυσόμενον"],
        ],
        col_labels=["Masculine", "Feminine", "Neuter"],
        row_labels=["Nominative", "Genitive", "Dative", "Accusative"],
    ),
    
    GridSpec(
        name="Future Passive Participle (Singular)",
        cell_texts=[
            ["λυθησόμενος", "λυθησομένη", "λυθησόμενον"],
            ["λυθησομένου", "λυθησομένης", "λυθησομένου"],
            ["λυθησομένῳ", "λυθησομένῃ", "λυθησομένῳ"],
            ["λυθησόμενον", "λυθησομένην", "λυθησόμενον"],
        ],
        col_labels=["Masculine", "Feminine", "Neuter"],
        row_labels=["Nominative", "Genitive", "Dative", "Accusative"],
    ),

]


# UI sizing tweaks (optional)
CELL_CHAR_WRAP = 200
CELL_WIDTH_CHARS = 18
CELL_HEIGHT_LINES = 3


# -----------------------------
# helpers
# -----------------------------

def _default_row_labels(n: int) -> list[str]:
    return [f"Row {i+1}" for i in range(n)]


def _default_col_labels(n: int) -> list[str]:
    return [f"Col {i+1}" for i in range(n)]


def _validate_rectangular(cell_texts: List[List[str]]):
    if not isinstance(cell_texts, list) or len(cell_texts) == 0:
        raise ValueError("cell_texts must be a non-empty 2D list.")
    if not all(isinstance(row, list) for row in cell_texts):
        raise ValueError("cell_texts must be a 2D list (list of lists).")
    row_lengths = [len(row) for row in cell_texts]
    if any(l == 0 for l in row_lengths):
        raise ValueError("cell_texts rows must not be empty.")
    if len(set(row_lengths)) != 1:
        raise ValueError("cell_texts must be rectangular: every row must have the same number of columns.")


def _normalize_labels(labels, n: int, default_fn):
    if labels is None:
        return default_fn(n)
    if not isinstance(labels, list) or len(labels) != n:
        return default_fn(n)
    return labels


# -----------------------------
# game
# -----------------------------

class RevealGame:
    def __init__(self, root: tk.Tk, grids: List[GridSpec]):
        self.root = root
        self.root.title("Reveal Grid Game")
        self.root.resizable(True, True)

        if not grids:
            raise ValueError("GRIDS must have at least one GridSpec.")
        for g in grids:
            _validate_rectangular(g.cell_texts)

        self.grids = grids
        self.current_grid: GridSpec = self.grids[0]

        # state (populated in reset_game)
        self.rows = 0
        self.cols = 0
        self.row_labels: List[str] = []
        self.col_labels: List[str] = []
        self.uncovered: List[List[bool]] = []
        self.active_cell = None
        self.active_revealed = False
        self.turns = 0
        self.correct = 0
        self.incorrect = 0
        self.start_time = None
        self.end_time = None
        self._timer_running = False

        # widgets
        self.frame = None
        self.header_frame = None
        self.grid_frame = None
        self.info_var = tk.StringVar()
        self.info_label = None
        self.instructions = None
        self.cell_widgets: List[List[tk.Label]] = []

        # dropdown var
        self.grid_choice_var = tk.StringVar(value=self.current_grid.name)

        self._build_ui()
        self._bind_keys()

        self.set_grid_by_name(self.current_grid.name)

    # -------- UI build --------
    def _build_ui(self):
        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Top header: dropdown + info
        self.header_frame = tk.Frame(self.frame)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(1, weight=1)

        tk.Label(self.header_frame, text="Grid:", font=("Helvetica", 11, "bold")).grid(
            row=0, column=0, sticky="w", padx=(0, 6)
        )

        choices = [g.name for g in self.grids]
        self.dropdown = tk.OptionMenu(
            self.header_frame,
            self.grid_choice_var,
            *choices,
            command=lambda name: self.set_grid_by_name(name),
        )
        self.dropdown.grid(row=0, column=1, sticky="w")

        # Info label
        self.info_label = tk.Label(self.frame, textvariable=self.info_var, justify="left", anchor="w")
        self.info_label.grid(row=1, column=0, sticky="w", pady=(8, 8))

        # Grid container (rebuilt when switching grids)
        self.grid_frame = tk.Frame(self.frame)
        self.grid_frame.grid(row=2, column=0, sticky="nsew")
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Instructions
        self.instructions = tk.Label(
            self.frame,
            text="Controls: SPACE reveal | ← Incorrect | → Correct  (optional: A/D)\nClick the window first so it receives key presses.",
            justify="left",
            anchor="w",
        )
        self.instructions.grid(row=3, column=0, sticky="w", pady=(8, 0))

    def _bind_keys(self):
        self.root.bind("<space>", lambda e: self.reveal_active())
        self.root.bind("<Left>", lambda e: self.handle_guess(is_correct=False))
        self.root.bind("<Right>", lambda e: self.handle_guess(is_correct=True))
        self.root.bind("a", lambda e: self.handle_guess(is_correct=False))
        self.root.bind("d", lambda e: self.handle_guess(is_correct=True))

    # -------- grid switching / rebuilding --------
    def set_grid_by_name(self, name: str):
        match = next((g for g in self.grids if g.name == name), None)
        if match is None:
            return
        self.current_grid = match
        self.grid_choice_var.set(match.name)
        self.reset_game()

    def reset_game(self):
        # stop timer
        self._timer_running = False

        # recompute dimensions/labels/state
        cell_texts = self.current_grid.cell_texts
        self.rows = len(cell_texts)
        self.cols = len(cell_texts[0])
        self.row_labels = _normalize_labels(self.current_grid.row_labels, self.rows, _default_row_labels)
        self.col_labels = _normalize_labels(self.current_grid.col_labels, self.cols, _default_col_labels)

        self.uncovered = [[False] * self.cols for _ in range(self.rows)]
        self.active_cell = None
        self.active_revealed = False

        self.turns = 0
        self.correct = 0
        self.incorrect = 0

        self.start_time = None
        self.end_time = None

        # rebuild visible grid widgets
        self._rebuild_grid_widgets()

        # start game
        self.next_turn()

    def _rebuild_grid_widgets(self):
        # clear previous grid
        for child in list(self.grid_frame.winfo_children()):
            child.destroy()

        # corner
        corner = tk.Label(self.grid_frame, text="", width=max(10, int(CELL_WIDTH_CHARS * 0.6)))
        corner.grid(row=0, column=0, padx=2, pady=2)

        # column labels
        for c, label in enumerate(self.col_labels):
            lbl = tk.Label(
                self.grid_frame,
                text=label,
                width=CELL_WIDTH_CHARS,
                padx=4,
                pady=4,
                font=("Helvetica", 11, "bold"),
            )
            lbl.grid(row=0, column=c + 1, padx=2, pady=2, sticky="nsew")

        # rows + cells
        self.cell_widgets = [[None] * self.cols for _ in range(self.rows)]
        for r, rlabel in enumerate(self.row_labels):
            rl = tk.Label(
                self.grid_frame,
                text=rlabel,
                width=max(10, int(CELL_WIDTH_CHARS * 0.6)),
                padx=4,
                pady=4,
                font=("Helvetica", 11, "bold"),
                anchor="e",
            )
            rl.grid(row=r + 1, column=0, padx=2, pady=2, sticky="nsew")

            for c in range(self.cols):
                w = tk.Label(
                    self.grid_frame,
                    text="",
                    width=CELL_WIDTH_CHARS,
                    height=CELL_HEIGHT_LINES,
                    relief="solid",
                    borderwidth=1,
                    font=("Helvetica", 16),
                    wraplength=CELL_CHAR_WRAP,
                    justify="center",
                )
                w.grid(row=r + 1, column=c + 1, padx=2, pady=2, sticky="nsew")
                self.cell_widgets[r][c] = w

        # make grid expand
        for r in range(self.rows + 1):
            self.grid_frame.grid_rowconfigure(r, weight=1)
        for c in range(self.cols + 1):
            self.grid_frame.grid_columnconfigure(c, weight=1)

        self._redraw()

    # -------- gameplay --------
    def _covered_positions(self):
        return [(r, c) for r in range(self.rows) for c in range(self.cols) if not self.uncovered[r][c]]

    def _start_timer_if_needed(self):
        if self.start_time is None:
            self.start_time = time.monotonic()
            self._timer_running = True
            self._tick_timer()

    def _elapsed_seconds(self):
        if self.start_time is None:
            return 0.0
        if self.end_time is not None:
            return max(0.0, self.end_time - self.start_time)
        return max(0.0, time.monotonic() - self.start_time)

    def _format_elapsed(self):
        secs = self._elapsed_seconds()
        minutes = int(secs // 60)
        rem = secs - minutes * 60
        return f"{minutes}:{rem:05.2f}"

    def _tick_timer(self):
        if not self._timer_running:
            return
        self._redraw()
        self.root.after(100, self._tick_timer)

    def next_turn(self):
        covered = self._covered_positions()
        if not covered:
            self.active_cell = None
            self.active_revealed = False
            self.end_time = time.monotonic()
            self._timer_running = False
            self._redraw()

            total_time = self._format_elapsed()
            messagebox.showinfo(
                "Game Over",
                "All cells uncovered!\n\n"
                f"Grid: {self.current_grid.name}\n"
                f"Turns: {self.turns}\n"
                f"Correct: {self.correct}\n"
                f"Incorrect: {self.incorrect}\n"
                f"Total time: {total_time}",
            )
            return

        self.turns += 1
        self.active_cell = random.choice(covered)
        self.active_revealed = False

        self._start_timer_if_needed()
        self._redraw()

    def reveal_active(self):
        if self.active_cell is None or self.active_revealed:
            return
        self.active_revealed = True
        self._redraw()

    def handle_guess(self, is_correct: bool):
        if self.active_cell is None:
            return
        if not self.active_revealed:
            return

        r, c = self.active_cell
        if is_correct:
            self.uncovered[r][c] = True
            self.correct += 1
        else:
            self.incorrect += 1

        self.active_cell = None
        self.active_revealed = False
        self._redraw()
        self.root.after(250, self.next_turn)

    # -------- rendering --------
    def _cell_display_text(self, r, c):
        cell_texts = self.current_grid.cell_texts
        if self.uncovered[r][c]:
            return str(cell_texts[r][c])
        if self.active_cell == (r, c) and self.active_revealed:
            return str(cell_texts[r][c])
        return "•••"

    def _redraw(self):
        remaining = len(self._covered_positions())
        elapsed = self._format_elapsed()
        time_line = f"Total time: {elapsed}" if (remaining == 0 and self.end_time is not None) else f"Elapsed: {elapsed}"

        if remaining == 0 and self.end_time is not None:
            status = "Finished."
        elif self.active_cell is None:
            status = "Picking next cell..."
        else:
            ar, ac = self.active_cell
            if not self.active_revealed:
                status = (
                    f"Turn {self.turns}: Highlighted ({self.row_labels[ar]}, {self.col_labels[ac]}). "
                    "Press SPACE to reveal."
                )
            else:
                status = (
                    f"Turn {self.turns}: Revealed ({self.row_labels[ar]}, {self.col_labels[ac]}). "
                    "← Incorrect / → Correct"
                )

        self.info_var.set(
            f"Grid: {self.current_grid.name}\n"
            f"{status}\n"
            f"Score: Correct {self.correct} | Incorrect {self.incorrect} | Remaining {remaining} | {time_line}"
        )

        for r in range(self.rows):
            for c in range(self.cols):
                w = self.cell_widgets[r][c]
                w.configure(
                    text=self._cell_display_text(r, c),
                    fg="black"   # ← FORCE TEXT COLOR
                )

                if self.active_cell == (r, c):
                    w.configure(bg="#fff2a8", relief="solid", borderwidth=2)
                elif self.uncovered[r][c]:
                    w.configure(bg="grey", relief="solid", borderwidth=1)
                else:
                    w.configure(bg="#f2f2f2", relief="solid", borderwidth=1)


def main():
    root = tk.Tk()
    RevealGame(root, GRIDS)
    root.mainloop()


if __name__ == "__main__":
    main()
