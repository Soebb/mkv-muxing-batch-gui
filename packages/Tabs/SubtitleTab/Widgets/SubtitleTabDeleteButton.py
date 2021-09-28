from pathlib import Path

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QPushButton, QFileDialog

from packages.Startup import GlobalFiles
from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.SubtitleTab.Widgets.ClearSubtitleFilesDialog import ClearSubtitleFilesDialog
from packages.Tabs.SubtitleTab.Widgets.ClearSubtitleTabDialog import ClearSubtitleTabDialog


class SubtitleTabDeleteButton(QPushButton):
    remove_tab_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setIcon(GlobalFiles.TrashIcon)
        self.hint_when_enabled = "Remove Tab"
        self.setToolTip(self.hint_when_enabled)
        self.clicked.connect(self.open_delete_tab_dialog)
        self.is_there_old_files = False

    def set_is_there_old_file(self, new_state):
        self.is_there_old_files = new_state

    def open_delete_tab_dialog(self):
        if self.is_there_old_files:
            clear_files_dialog = ClearSubtitleTabDialog()
            clear_files_dialog.execute()
            if clear_files_dialog.result == "Yes":
                self.remove_tab_signal.emit()
        else:
            self.remove_tab_signal.emit()

    def setEnabled(self, new_state: bool):
        super().setEnabled(new_state)
        if not new_state and not GlobalSetting.JOB_QUEUE_EMPTY:
            if self.hint_when_enabled != "":
                self.setToolTip("<nobr>" + self.hint_when_enabled + "<br>" + GlobalSetting.DISABLE_TOOLTIP)
            else:
                self.setToolTip("<nobr>" + GlobalSetting.DISABLE_TOOLTIP)
        else:
            self.setToolTip(self.hint_when_enabled)

    def setDisabled(self, new_state: bool):
        super().setDisabled(new_state)
        if new_state and not GlobalSetting.JOB_QUEUE_EMPTY:
            if self.hint_when_enabled != "":
                self.setToolTip("<nobr>" + self.hint_when_enabled + "<br>" + GlobalSetting.DISABLE_TOOLTIP)
            else:
                self.setToolTip("<nobr>" + GlobalSetting.DISABLE_TOOLTIP)
        else:
            self.setToolTip(self.hint_when_enabled)

    def setToolTip(self, new_tool_tip: str):
        if self.isEnabled() or GlobalSetting.JOB_QUEUE_EMPTY:
            self.hint_when_enabled = new_tool_tip
        super().setToolTip(new_tool_tip)
