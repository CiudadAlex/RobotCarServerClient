from remotecontrolui.RemoteControlUI import RemoteControlUI
from engine.Engine import Engine


online = True


if __name__ == "__main__":
    Engine.start(car_speaks=False,
                 commands_by_audio=True,
                 connect_to_video_stream=online,
                 connect_to_audio_or_text_command_stream=online)

    RemoteControlUI.launch()


# FIXME test: follow me
# FIXME test: Limit of 4 secs to send audio to speech recognition
# FIXME test: ComplexCommandPhotoDoor

# FIXME Room recognizer: More photographs if doubt
# FIXME selector of room and door in UI Web


# FIXME Command: Go to room
# FIXME Speakers to answer
# FIXME LLM with contexts




