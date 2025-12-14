import sys
import os
import pygame
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QVBoxLayout,QHBoxLayout,QListWidget,QPushButton,QSlider
from PyQt5.QtCore import Qt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUSIC_FOLDER = os.path.join(BASE_DIR, "music")

pygame.mixer.init()

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Music_Player")
window.setGeometry(500,500,500,300)
window.setStyleSheet("""
    QWidget {
        background-color: #0c343d;
        color: white;
        font-size: 16px;
    }
    QListWidget {
        background-color: #2b2b2b;
        border: 1px solid #444;
    }
    QPushButton {
        background-color: #333;
        border: 1px solid #555;
        padding: 8px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #444;
    }
""")

label=QLabel("Please select a song and click play")


song_list=QListWidget()
for song in os.listdir(MUSIC_FOLDER):
    if song.endswith(".mp3"):
        song_list.addItem(song)

play_button=QPushButton("Play")
pause_button=QPushButton("Pause")
resume_button=QPushButton("Resume")
stop_button=QPushButton("Stop")
next_button=QPushButton("Next")
previous_button=QPushButton("Previous")

volume_slider=QSlider(Qt.Horizontal)
volume_slider.setRange(0,100)
volume_slider.setValue(40)

def play_clicked():
    selected_item=song_list.currentItem()
    if selected_item is None:
        label.setText("please select a song")
        return
    
    song_name=selected_item.text()
    file_path=os.path.join(MUSIC_FOLDER,song_name)


    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


    label.setText(f"Playing: {song_name}")

def pause_clicked():
    pygame.mixer.music.pause()
 

def resume_clicked():
    pygame.mixer.music.unpause()


def stop_clicked():
    pygame.mixer.music.stop()

def next_clicked():
    current_row=song_list.currentRow()
    total=song_list.count()

    if current_row<total-1:
        song_list.setCurrentRow(current_row+1)
        play_clicked()
    else:
        label.setText("This is the Last Song")

def previous_clicked():
    current_row=song_list.currentRow()

    if current_row>0:
        song_list.setCurrentRow(current_row-1)
        play_clicked() 
    else:
        label.setText("This is the first song")

def change_volume(value):
    pygame.mixer.music.set_volume(value/100)

play_button.clicked.connect(play_clicked)
pause_button.clicked.connect(pause_clicked)
resume_button.clicked.connect(resume_clicked)
stop_button.clicked.connect(stop_clicked)
next_button.clicked.connect(next_clicked)
previous_button.clicked.connect(previous_clicked)
volume_slider.valueChanged.connect(change_volume)

layout=QVBoxLayout()
layout.addWidget(label)
layout.addWidget(song_list)
layout.addWidget(volume_slider)

button_layout=QHBoxLayout()
button_layout.addWidget(previous_button)
button_layout.addWidget(play_button)
button_layout.addWidget(pause_button)
button_layout.addWidget(resume_button)
button_layout.addWidget(stop_button)
button_layout.addWidget(next_button)


layout.addLayout(button_layout)
window.setLayout(layout)

window.show()
sys.exit(app.exec_())