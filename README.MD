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