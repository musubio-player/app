package main

import (
	"time"
)

type SearchResult struct {
	SearchItems   []SearchItem `json:"items"`
	NextPageToken string       `json:"nextPageToken"`
}

type SearchItem struct {
	Title                string    `json:"title"`
	VideoId              string    `json:"videoId"`
	VideoURL             string    `json:"videoURL"`
	Kind                 string    `json:"kind"`
	ChannelId            string    `json:"channelId"`
	ChannelTitle         string    `json:"channelTitle"`
	Description          string    `json:"description"`
	PublishedAt          time.Time `json:"publishedAt"`
	LiveBroadcastContent string    `json:"liveBroadcastContent"`
	ThumbnailDefaultURL  string    `json:"thumbnailDefaultURL"`
	ThumbnailHighURL     string    `json:"thumbnailHighURL"`
	ThumbnailMediumURL   string    `json:"thumbnailMediumURL"`
}
