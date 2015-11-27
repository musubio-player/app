package main

import (
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	//	"os"
	"time"

	"code.google.com/p/google-api-go-client/googleapi/transport"
	"code.google.com/p/google-api-go-client/youtube/v3"
	log "github.com/Sirupsen/logrus"
	"github.com/gorilla/mux"
)

const developerKey = "AIzaSyDfvJI8TlhqvWYEWSgyskBc2lKvGqPUUQk"

func Index(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "Welcome!")
}

func SearchIndex(w http.ResponseWriter, r *http.Request) {
	q := r.URL.Query().Get("q")

	client := &http.Client{
		Transport: &transport.APIKey{Key: developerKey},
	}

	service, err := youtube.New(client)
	if err != nil {
		log.Fatalf("Error creating new YouTube client: %v", err)
	}

	// Make the API call to YouTube.
	call := service.Search.List("id,snippet").
		Q(q).
		MaxResults(25)
	response, err := call.Do()

	if err != nil {
		log.Fatalf("Error making search API call: %v", err)
	}

	// Group video, channel, and playlist results in separate lists.
	videos := make(map[string]string)
	channels := make(map[string]string)
	playlists := make(map[string]string)

	var items []SearchItem

	// Iterate through each item and add it to the correct list.
	for _, item := range response.Items {
		switch item.Id.Kind {
		case "youtube#video":
			videos[item.Id.VideoId] = item.Snippet.Title

			publishedAt, err := time.Parse("2006-01-02T15:04:05.000Z", item.Snippet.PublishedAt)
			if err != nil {
				log.Fatalf("Error in the published date format", err)
			}

			item := SearchItem{
				Title:                item.Snippet.Title,
				VideoId:              item.Id.VideoId,
				VideoURL:             "https://www.youtube.com/watch?v=" + item.Id.VideoId,
				ChannelId:            item.Snippet.ChannelId,
				ChannelTitle:         item.Snippet.ChannelTitle,
				Description:          item.Snippet.Description,
				ThumbnailDefaultURL:  item.Snippet.Thumbnails.Default.Url,
				ThumbnailHighURL:     item.Snippet.Thumbnails.High.Url,
				ThumbnailMediumURL:   item.Snippet.Thumbnails.Medium.Url,
				PublishedAt:          publishedAt,
				LiveBroadcastContent: item.Snippet.LiveBroadcastContent,
			}
			items = append(items, item)

		case "youtube#channel":
			channels[item.Id.ChannelId] = item.Snippet.Title
		case "youtube#playlist":
			playlists[item.Id.PlaylistId] = item.Snippet.Title
		}
	}

	result := SearchResult{
		NextPageToken: response.NextPageToken,
		SearchItems:   items,
	}

	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.Header().Set("Access-Control-Allow-Origin", "http://local.musubio.com")
	w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
	w.Header().Set("Access-Control-Allow-Headers", "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")
	w.WriteHeader(http.StatusOK)

	if err := json.NewEncoder(w).Encode(result); err != nil {
		panic(err)
	}
}

func TodoIndex(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)

	if err := json.NewEncoder(w).Encode(todos); err != nil {
		panic(err)
	}
}

func TodoShow(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	todoId := vars["todoId"]
	fmt.Fprintln(w, "Todo show:", todoId)
}

func TodoCreate(w http.ResponseWriter, r *http.Request) {
	var todo Todo
	body, err := ioutil.ReadAll(io.LimitReader(r.Body, 1048576))

	if err != nil {
		panic(err)
	}

	if err := r.Body.Close(); err != nil {
		panic(err)
	}

	if err := json.Unmarshal(body, &todo); err != nil {
		w.Header().Set("Content-Type", "application/json; charset=UTF-8")
		w.WriteHeader(422) // unprocessable entity
		if err := json.NewEncoder(w).Encode(err); err != nil {
			panic(err)
		}
	}

	t := RepoCreateTodo(todo)
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusCreated)
	if err := json.NewEncoder(w).Encode(t); err != nil {
		panic(err)
	}
}
