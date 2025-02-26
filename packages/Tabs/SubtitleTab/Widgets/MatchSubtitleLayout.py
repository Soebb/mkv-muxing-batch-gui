from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout

from packages.Tabs.GlobalSetting import GlobalSetting
from packages.Tabs.SubtitleTab.Widgets.MatchSubtitleToolsLayout import MatchSubtitleToolsLayout
from packages.Tabs.SubtitleTab.Widgets.SubtitleMatchingTable import SubtitleMatchingTable
from packages.Tabs.SubtitleTab.Widgets.VideoMatchingTable import VideoMatchingTable


class MatchSubtitleLayout(QHBoxLayout):
    sync_subtitle_files_with_global_files_after_swap_delete_signal = Signal()

    def __init__(self, tab_index, parent=None):
        super().__init__()
        self.tab_index = tab_index
        self.video_table = VideoMatchingTable()
        self.subtitle_table = SubtitleMatchingTable(self.tab_index)
        self.match_tools_layout = MatchSubtitleToolsLayout(parent=parent, tab_index=self.tab_index)
        self.setup_layout()
        self.sync_slideBar_check = False
        self.connect_signals()

    def connect_signals(self):
        self.subtitle_table.table.selectionModel().selectionChanged.connect(
            self.sync_selection_between_subtitles_and_videos
        )
        self.subtitle_table.table.selectionModel().selectionChanged.connect(
            self.send_selection_to_tools_layout
        )
        self.match_tools_layout.refresh_subtitle_table_signal.connect(self.show_subtitle_files_after_swapping_deleting)
        self.match_tools_layout.selected_subtitle_row_signal.connect(self.change_selected_subtitle_row)

    def setup_layout(self):
        self.addWidget(self.video_table, 50)
        self.addSpacing(10)
        self.addLayout(self.match_tools_layout, 4)
        self.addSpacing(10)
        self.addWidget(self.subtitle_table, 50)

    def sync_slideBar(self):
        if self.sync_slideBar_check == True or self.subtitle_table.table.verticalScrollBar().isSliderDown():
            self.video_table.table.verticalScrollBar().setValue(
                self.subtitle_table.table.verticalScrollBar().value()
            )
            self.sync_slideBar_check = False

    def sync_selection_between_subtitles_and_videos(self):
        list_of_selected_rows = self.subtitle_table.table.selectionModel().selectedRows()
        video_file_list = GlobalSetting.VIDEO_FILES_LIST
        if len(list_of_selected_rows):
            selected_row = list_of_selected_rows[0].row()
            if len(video_file_list) - 1 >= selected_row:
                self.video_table.table.preventSelect = False
                oldHorizontalScrollBarValue = (
                    self.video_table.table.horizontalScrollBar().value()
                )
                self.video_table.table.selectRow(selected_row)
                self.video_table.table.horizontalScrollBar().setValue(
                    oldHorizontalScrollBarValue
                )
                self.video_table.table.preventSelect = True
                self.sync_slideBar_check = True
            else:
                self.video_table.table.clearSelection()
                return
        else:
            self.video_table.table.clearSelection()
            return

    def send_selection_to_tools_layout(self):
        selected_row = -1
        max_index = len(GlobalSetting.SUBTITLE_FILES_LIST[self.tab_index]) - 1
        list_of_selected_rows = self.subtitle_table.table.selectionModel().selectedRows()
        if len(list_of_selected_rows) > 0:
            selected_row = list_of_selected_rows[0].row()
        self.match_tools_layout.set_selected_row(selected_row=selected_row, max_index=max_index)

    def show_video_files(self):
        self.video_table.show_files()

    def show_subtitle_files(self):
        self.sync_subtitle_files_with_global_files_after_swap_delete_signal.emit()
        self.subtitle_table.show_files()

    def show_subtitle_files_after_swapping_deleting(self):
        self.sync_subtitle_files_with_global_files_after_swap_delete_signal.emit()
        self.subtitle_table.show_files_after_swapping_deleting()

    def change_selected_subtitle_row(self, new_selected_row):
        self.subtitle_table.select_row(new_selected_row)

    def clear_tables(self):
        self.video_table.clear_table()
        self.subtitle_table.clear_table()

    def clear_subtitle_selection(self):
        self.subtitle_table.clear_selection()

    def disable_editable_widgets(self):
        self.subtitle_table.table.setAcceptDrops(False)
        self.match_tools_layout.disable_editable_widgets()

    def enable_editable_widgets(self):
        self.subtitle_table.table.setAcceptDrops(True)
        self.match_tools_layout.enable_editable_widgets()
