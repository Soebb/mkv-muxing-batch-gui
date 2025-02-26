#import faulthandler
from PySide6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QStyleFactory, \
    QGridLayout, QLabel

from packages.Startup.Options import Options
from packages.Startup.MainApplication import get_dark_palette, get_light_palette
from packages.Startup.PreDefined import AllVideosExtensions, AllSubtitlesExtensions, AllAudiosExtensions, \
    AllChapterExtensions
from packages.Tabs.SettingTab.Widgets.DefaultDirectoryLayout import DefaultDirectoryLayout
from packages.Tabs.SettingTab.Widgets.DefaultExtensionsLayout import DefaultExtensionsLayout
from packages.Tabs.SettingTab.Widgets.DefaultLanguageLayout import DefaultLanguageLayout
from packages.Widgets.SingleDefaultPresetsData import SingleDefaultPresetsData

#faulthandler.enable()


def try_to_create_windows_vista_style():
    style = QStyleFactory.create("windowsvista")
    if str(style.__class__).find("PySide6.QtGui.QStandardItem") != -1:
        return try_to_create_windows_vista_style()
    return style


class PresetTabWidget(QWidget):
    def __init__(self, options):
        super().__init__()
        self.options: SingleDefaultPresetsData = options
        self.default_directories_groupBox = QGroupBox(self)
        self.default_extensions_groupBox = QGroupBox(self)
        self.default_languages_groupBox = QGroupBox(self)
        self.default_directories_layout = QVBoxLayout()
        self.default_extensions_layout = QGridLayout()
        self.default_languages_layout = QGridLayout()
        self.default_languages_layout_spacer_item = None
        self.default_video_directory_layout = DefaultDirectoryLayout(
            label_name="Videos Directory: ",
            default_directory=self.options.Default_Video_Directory
        )
        self.default_subtitle_directory_layout = DefaultDirectoryLayout(
            label_name="Subtitles Directory: ",
            default_directory=self.options.Default_Subtitle_Directory
        )
        self.default_audio_directory_layout = DefaultDirectoryLayout(
            label_name="Audios Directory: ",
            default_directory=self.options.Default_Audio_Directory
        )
        self.default_chapter_directory_layout = DefaultDirectoryLayout(
            label_name="Chapters Directory: ",
            default_directory=self.options.Default_Chapter_Directory
        )
        self.default_attachment_directory_layout = DefaultDirectoryLayout(
            label_name="Attachments Directory: ",
            default_directory=self.options.Default_Attachment_Directory
        )
        self.default_destination_directory_layout = DefaultDirectoryLayout(
            label_name="Destination Directory: ",
            default_directory=self.options.Default_Destination_Directory
        )
        self.default_video_extensions_layout = DefaultExtensionsLayout(
            label_name="Video Extensions: ",
            extensions_list=AllVideosExtensions,
            default_extensions_list=self.options.Default_Video_Extensions
        )
        self.default_subtitle_extensions_layout = DefaultExtensionsLayout(
            label_name="Subtitle Extensions: ",
            extensions_list=AllSubtitlesExtensions,
            default_extensions_list=self.options.Default_Subtitle_Extensions
        )
        self.default_audio_extensions_layout = DefaultExtensionsLayout(
            label_name="Audio Extensions: ",
            extensions_list=AllAudiosExtensions,
            default_extensions_list=self.options.Default_Audio_Extensions
        )
        self.default_chapter_extensions_layout = DefaultExtensionsLayout(
            label_name="Chapter Extensions: ",
            extensions_list=AllChapterExtensions,
            default_extensions_list=self.options.Default_Chapter_Extensions
        )

        self.default_subtitle_language_layout = DefaultLanguageLayout(
            label_name="Subtitle Language: ",
            languages_list=self.options.Default_Favorite_Subtitle_Languages,
            default_language=self.options.Default_Subtitle_Language
        )
        self.default_audio_language_layout = DefaultLanguageLayout(
            label_name="Audio Language: ",
            languages_list=self.options.Default_Favorite_Audio_Languages,
            default_language=self.options.Default_Audio_Language
        )
        self.main_layout = QVBoxLayout()
        self.setup_main_layout()
        self.setLayout(self.main_layout)
        self.connect_signals()
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    def setup_main_layout(self):
        self.setup_default_directories_groupBox()
        self.setup_default_extensions_groupBox()
        self.setup_default_languages_groupBox()
        self.setup_default_directories_layout()
        self.setup_default_extensions_layout()
        self.setup_default_languages_layout()
        self.main_layout.addWidget(self.default_directories_groupBox, stretch=0)
        self.main_layout.addWidget(self.default_extensions_groupBox, stretch=0)
        self.main_layout.addWidget(self.default_languages_groupBox, stretch=0)

    def setup_default_directories_groupBox(self):
        self.default_directories_groupBox.setStyle(try_to_create_windows_vista_style())
        self.default_directories_groupBox.setTitle("Default Directories")
        self.default_directories_groupBox.setLayout(self.default_directories_layout)
        if Options.Dark_Mode:
            self.default_directories_groupBox.setPalette(get_dark_palette())
        else:
            self.default_directories_groupBox.setPalette(get_light_palette())

    def setup_default_extensions_groupBox(self):
        self.default_extensions_groupBox.setStyle(try_to_create_windows_vista_style())
        self.default_extensions_groupBox.setTitle("Default Extensions")
        self.default_extensions_groupBox.setLayout(self.default_extensions_layout)
        if Options.Dark_Mode:
            self.default_extensions_groupBox.setPalette(get_dark_palette())
        else:
            self.default_extensions_groupBox.setPalette(get_light_palette())

    def setup_default_languages_groupBox(self):
        self.default_languages_groupBox.setStyle(try_to_create_windows_vista_style())
        self.default_languages_groupBox.setTitle("Favorite Languages List")
        self.default_languages_groupBox.setLayout(self.default_languages_layout)
        if Options.Dark_Mode:
            self.default_languages_groupBox.setPalette(get_dark_palette())
        else:
            self.default_languages_groupBox.setPalette(get_light_palette())

    def setup_default_directories_layout(self):
        self.default_directories_layout.addLayout(self.default_video_directory_layout)
        self.default_directories_layout.addLayout(self.default_subtitle_directory_layout)
        self.default_directories_layout.addLayout(self.default_audio_directory_layout)
        self.default_directories_layout.addLayout(self.default_chapter_directory_layout)
        self.default_directories_layout.addLayout(self.default_attachment_directory_layout)
        self.default_directories_layout.addLayout(self.default_destination_directory_layout)

    def setup_default_extensions_layout(self):
        self.default_extensions_layout.addLayout(self.default_video_extensions_layout, 0, 0)
        self.default_extensions_layout.addLayout(self.default_subtitle_extensions_layout, 0, 1)
        self.default_extensions_layout.addLayout(self.default_audio_extensions_layout, 1, 0)
        self.default_extensions_layout.addLayout(self.default_chapter_extensions_layout, 1, 1)

    def setup_default_languages_layout(self):
        self.default_languages_layout_spacer_item = QLabel()
        self.default_languages_layout.addWidget(self.default_subtitle_language_layout.label, 0, 0)
        self.default_languages_layout.addWidget(self.default_subtitle_language_layout.languages_comboBox, 0, 1)
        self.default_languages_layout.addWidget(self.default_subtitle_language_layout.setting_button, 0, 2)
        self.default_languages_layout.addWidget(self.default_languages_layout_spacer_item, 0, 3)
        self.default_languages_layout.addWidget(self.default_audio_language_layout.label, 0, 4)
        self.default_languages_layout.addWidget(self.default_audio_language_layout.languages_comboBox, 0, 5)
        self.default_languages_layout.addWidget(self.default_audio_language_layout.setting_button, 0, 6)
        self.default_languages_layout.setColumnStretch(0, 0)
        self.default_languages_layout.setColumnStretch(1, 1)
        self.default_languages_layout.setColumnStretch(2, 0)
        self.default_languages_layout.setColumnStretch(3, 0)
        self.default_languages_layout.setColumnStretch(4, 0)
        self.default_languages_layout.setColumnStretch(5, 1)
        self.default_languages_layout.setColumnStretch(6, 0)

    def connect_signals(self):
        pass

    def get_current_options_as_option_data(self) -> SingleDefaultPresetsData:
        self.options.Default_Video_Directory = self.default_video_directory_layout.lineEdit.text()
        self.options.Default_Subtitle_Directory = self.default_subtitle_directory_layout.lineEdit.text()
        self.options.Default_Audio_Directory = self.default_audio_directory_layout.lineEdit.text()
        self.options.Default_Chapter_Directory = self.default_chapter_directory_layout.lineEdit.text()
        self.options.Default_Attachment_Directory = self.default_attachment_directory_layout.lineEdit.text()
        self.options.Default_Destination_Directory = self.default_destination_directory_layout.lineEdit.text()

        self.options.Default_Video_Extensions = self.default_video_extensions_layout.extensions_checkable_comboBox.currentData()
        self.options.Default_Subtitle_Extensions = self.default_subtitle_extensions_layout.extensions_checkable_comboBox.currentData()
        self.options.Default_Audio_Extensions = self.default_audio_extensions_layout.extensions_checkable_comboBox.currentData()
        self.options.Default_Chapter_Extensions = self.default_chapter_extensions_layout.extensions_checkable_comboBox.currentData()

        self.options.Default_Subtitle_Language = self.default_subtitle_language_layout.languages_comboBox.currentText()
        self.options.Default_Audio_Language = self.default_audio_language_layout.languages_comboBox.currentText()

        self.options.Default_Favorite_Subtitle_Languages = self.default_subtitle_language_layout.current_languages_list.copy()
        self.options.Default_Favorite_Audio_Languages = self.default_audio_language_layout.current_languages_list.copy()
        return self.options
