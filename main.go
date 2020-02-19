package main

import (
	"net/http"

	"github.com/globalsign/mgo"
	"github.com/santosh/eldiario/handler"
	"goji.io"
	"goji.io/pat"
)


// TODO: Can we replace goji with mux? Which one is better?
func main() {
	session, err := mgo.Dial("localhost")
	if err != nil {
		panic(err)
	}
	defer session.Close()

	session.SetMode(mgo.Monotonic, true)
	ensureIndex(session)

	mux := goji.NewMux()
	mux.HandleFunc(pat.Get("/entry"), handler.GetEntries(session))
	mux.HandleFunc(pat.Post("/entry"), handler.CreateEntry(session))
	mux.HandleFunc(pat.Get("/entry/:id"), handler.GetEntry(session))
	mux.HandleFunc(pat.Put("/entry/:id"), handler.UpdateEntry(session))
	mux.HandleFunc(pat.Delete("/entry/:id"), handler.DeleteEntry(session))
	
	// shoud be at last; otherwise other patterns never gonna match
	mux.Handle(pat.Get("/"), http.StripPrefix("/", http.FileServer(http.Dir("static"))))

	http.ListenAndServe(":8080", mux)
}

func ensureIndex(s *mgo.Session) {
	session := s.Copy()
	defer session.Close()

	c := session.DB("eldiario").C("entries")

	index := mgo.Index{
		// TODO: Can we please use mongo's native _id?
		Key:        []string{"id"},
		Unique:     true,
		DropDups:   true,
		Background: true,
		Sparse:     true,
	}

	err := c.EnsureIndex(index)
	if err != nil {
		panic(err)
	}
}
