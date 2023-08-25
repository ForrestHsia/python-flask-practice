20230824
更新 YT 播放清單的清查時間區段
update cpbl_youtube_data.cpbl_youtube_playlist
set cpbl_youtube_playlist.max_time = (SELECT max(video_date) FROM 庫.表 where is_fault is Null),
set cpbl_youtube_playlist.min_time = (SELECT min(video_date) FROM 庫.表 where is_fault is Null)
where cpbl_youtube_playlist.eng_title = 表;

