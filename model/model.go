package model

// Entry Struct (Model)
type Entry struct {
	// TODO: Can we please use mongo's native _id?
	ID       string `json:"id"`
	Body     string `json:"body"`
	Created  string `json:"created"`
	Modified string `json:"modified"`
	Author   string `json:"author"`
}
