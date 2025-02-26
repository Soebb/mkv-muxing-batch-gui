from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout

from packages.Tabs.GlobalSetting import convert_check_state_int_to_check_state
from packages.Tabs.VideoTab.Widgets.ModifyOldTracksWidgtes.TrackCheckBoxCell import TrackCheckBoxCell


class CenteredCheckBoxCell(QWidget):
    signal_state_changed = Signal(list)

    def __init__(self, row_id, column_id, check_state,parent=None):
        super().__init__(parent=parent)
        self.check_box = TrackCheckBoxCell(row_id=row_id, column_id=column_id)
        self.check_box.setCheckState(convert_check_state_int_to_check_state(check_state))
        self.mini_layout = QHBoxLayout()
        self.mini_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mini_layout.addWidget(self.check_box)
        self.mini_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mini_layout)
        self.check_box.signal_state_changed.connect(self.signal_state_changed.emit)
