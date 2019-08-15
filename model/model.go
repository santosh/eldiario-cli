package model

// Entry Struct (Model)
type Entry struct {
	// TODO: Can we please use mongo's native _id?
	ID       string `json:"id"`
	Body     string `json:"body"`
	Datetime string `json:"datetime"`
	Author   string `json:"author"`
}
