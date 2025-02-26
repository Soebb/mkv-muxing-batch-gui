import sys

import PySide6
from PySide6.QtCore import Signal
from PySide6.QtGui import Qt, QColor, QKeySequence, QShortcut
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem

from packages.Startup.Options import Options
from packages.Startup.InitializeScreenResolution import screen_size
from packages.Tabs.GlobalSetting import sort_names_like_windows, GlobalSetting
from packages.Widgets.TableWidget import TableWidget


class VideoTable(TableWidget):
    drop_folder_and_files_signal = Signal(list)
    update_unchecked_video_signal = Signal(int)
    update_checked_video_signal = Signal(int)
    move_video_to_down_signal = Signal(int)
    move_video_to_up_signal = Signal(int)

    def __init__(self):
        super().__init__()
        self.column_ids = {
            "Name": 0,
            "Size": 1,
        }
        self.text_color = {"light": {"activate": "#000000", "disable": "#787878"},
                           "dark": {"activate": "#FFFFFF", "disable": "#878787"}}
        self.setColumnCount(2)
        self.setRowCount(0)
        self.setAcceptDrops(True)
        self.checking_row_updates = True
        self.move_row_up_shortcut = None
        self.move_row_down_shortcut = None
        self.disable_table_bold_column()
        self.disable_table_edit()
        self.force_select_whole_row()
        self.force_single_row_selection()
        self.make_column_expand_as_possible(column_index=0)
        self.set_row_height(new_height=screen_size.height() // 27)
        self.setup_columns()
        self.setup_shortcuts()
        self.connect_signals()

    def setup_shortcuts(self):
        self.move_row_up_shortcut = QShortcut(QKeySequence("Ctrl+Up"), self)
        self.move_row_down_shortcut = QShortcut(QKeySequence("Ctrl+Down"), self)

    def connect_signals(self):
        self.itemChanged.connect(self.update_checked_videos_state)
        self.itemClicked.connect(self.update_selected_row)
        if GlobalSetting.JOB_QUEUE_EMPTY:
            self.move_row_up_shortcut.activated.connect(self.move_row_up)
            self.move_row_down_shortcut.activated.connect(self.move_row_down)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        paths_to_add = []
        for url in urls:
            if sys.platform == "win32":
                current_path = url.path()[1:]
            else:
                current_path = url.path()
            paths_to_add.append(current_path)

        self.drop_folder_and_files_signal.emit(sort_names_like_windows(paths_to_add))

    def disable_table_bold_column(self):
        self.horizontalHeader().setHighlightSections(False)

    def disable_table_edit(self):
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def force_select_whole_row(self):
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

    def make_column_expand_as_possible(self, column_index):
        header = self.horizontalHeader()
        header.setSectionResizeMode(column_index, QHeaderView.ResizeMode.Stretch)

    def force_single_row_selection(self):
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

    def setup_columns(self):
        self.set_column_name(column_index=0, name="Name")
        self.set_column_name(column_index=1, name="Size")

    def set_column_name(self, column_index, name):
        column = QTableWidgetItem(name)
        column.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.setHorizontalHeaderItem(column_index, column)

    def set_row_height(self, new_height):
        self.verticalHeader().setDefaultSectionSize(new_height)

    def resize_2nd_column(self):
        self.setColumnWidth(1, min(self.columnWidth(0) // 2, screen_size.width() // 14))

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        self.resize_2nd_column()

    def show_files_list(self, files_names_list, files_names_checked_list, files_size_list):
        self.setRowCount(len(files_names_list))
        self.set_row_height(new_height=screen_size.height() // 27)
        for i in range(len(files_names_list)):
            self.set_row_number(row_number=i + 1, row_index=i)
            self.set_row_file_name(file_name=files_names_list[i], row_index=i, is_checked=files_names_checked_list[i])
            self.set_row_file_size(file_size=files_size_list[i], row_index=i)
            if files_names_checked_list[i]:
                self.update_row_text_color(row_index=i, status="activate")
            else:
                self.update_row_text_color(row_index=i, status="disable")
        self.show()

    def set_row_number(self, row_number, row_index):
        row_number_item = QTableWidgetItem(str(row_number))
        row_number_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setVerticalHeaderItem(row_index, row_number_item)

    def set_row_file_size(self, file_size, row_index):
        file_size_item = QTableWidgetItem(file_size)
        self.setItem(row_index, 1, file_size_item)

    def set_row_file_name(self, file_name, row_index, is_checked=True):
        file_name_item = QTableWidgetItem(" " + file_name)
        if is_checked:
            file_name_item.setCheckState(Qt.CheckState.Checked)
        else:
            file_name_item.setCheckState(Qt.CheckState.Unchecked)
        self.setItem(row_index, 0, file_name_item)

    def update_checked_videos_state(self, item: QTableWidgetItem):
        video_index = item.row()
        if self.checking_row_updates:
            self.checking_row_updates = False
            self.update_selected_row(item=item)
            if item.checkState() == Qt.CheckState.Unchecked:
                self.update_row_text_color(row_index=video_index, status="disable")
                self.update_unchecked_video_signal.emit(video_index)
            elif item.checkState() == Qt.CheckState.Checked:
                self.update_row_text_color(row_index=video_index, status="activate")
                self.update_checked_video_signal.emit(video_index)
            self.checking_row_updates = True

    def update_video_theme(self, item: QTableWidgetItem):
        video_index = item.row()
        if item.checkState() == Qt.CheckState.Unchecked:
            self.update_row_text_color(row_index=video_index, status="disable")
        elif item.checkState() == Qt.CheckState.Checked:
            self.update_row_text_color(row_index=video_index, status="activate")

    def update_theme_mode_state(self):
        for i in reversed(range(self.rowCount())):
            self.update_video_theme(self.item(i, self.column_ids["Name"]))

    def update_row_text_color(self, row_index, status):
        if Options.Dark_Mode:
            new_color = QColor(self.text_color["dark"][status])
        else:
            new_color = QColor(self.text_color["light"][status])
        self.item(row_index, self.column_ids["Name"]).setForeground(new_color)
        self.item(row_index, self.column_ids["Size"]).setForeground(new_color)

    def update_selected_row(self, item):
        row_index = item.row()
        self.selectRow(row_index)

    def disable_selection(self):
        for i in reversed(range(self.rowCount())):
            self.item(i, self.column_ids["Name"]).setFlags(
                self.item(i, self.column_ids["Name"]).flags() & (~Qt.ItemFlag.ItemIsUserCheckable))

    def enable_selection(self):
        for i in reversed(range(self.rowCount())):
            self.item(i, self.column_ids["Name"]).setFlags(
                self.item(i, self.column_ids["Name"]).flags() | Qt.ItemFlag.ItemIsUserCheckable)

    def move_row_down(self):
        if not GlobalSetting.JOB_QUEUE_EMPTY:
            return
        if self.rowCount() == 0:
            return
        if self.currentRow() == (self.rowCount() - 1):
            return
        self.move_video_to_down_signal.emit(self.currentRow())

    def move_row_up(self):
        if not GlobalSetting.JOB_QUEUE_EMPTY:
            return
        if self.rowCount() == 0:
            return
        if self.currentRow() == 0:
            return
        self.move_video_to_up_signal.emit(self.currentRow())
