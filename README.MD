Download manually from [github](https://github.com/BtbN/FFmpeg-Builds/releases): ffmpeg-n7.1-latest-winarm64-gpl-7.1.zip

```shell
ffmpeg -list_devices true -f dshow -i dummy
```

```shell
ffmpeg -f dshow -i audio="CABLE Output (VB-Audio Virtual Cable)" my_recording1.wav
```

```shell
ffmpeg -f dshow -i audio="CABLE Output (VB-Audio Virtual Cable)" -c:a aac -b:a 64k meeting_recording.m4a
```

```shell
uv pip install torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu129
```

[https://pytorch.org/get-started/previous-versions/](https://pytorch.org/get-started/previous-versions/)

1. Install and Configure OBS Studio
    * Download and install OBS Studio from obsproject.com.
    * When you first launch it, choose "Optimize just for recording".
    * In the main window, under "Sources", remove any default sources like "Display Capture".
    * Add a new source by clicking the + button and selecting "Audio Output Capture". Name it "Desktop Audio" and select
      your default speakers or headphones.
2. Enable the WebSocket Server
    * In OBS, go to Tools -> WebSocket Server Settings.
    * Check "Enable WebSocket Server".
    * You can leave the port as 4455.•
    * Click "Show Connect Info" and note down the Server Password. You will need this for your script.

3. Configure for Audio-Only Recording
    * Go to File -> Settings -> Output.
    * Change Output Mode to "Advanced".
    * Go to the "Recording" tab.
        * Set Type to "Standard".
        * Set a Recording Path where your files will be saved.
        * For the Audio Track, make sure only track 1 is checked.
        * Set the Encoder to FFmpeg AAC.