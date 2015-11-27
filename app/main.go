package main

import (
	"net/http"

	log "github.com/Sirupsen/logrus"
)

func main() {
	port := "8888"
	router := NewRouter()

	log.Info("HTTP server started at http://localhost:" + port)
	log.Fatal(http.ListenAndServe(":"+port, router))
}
