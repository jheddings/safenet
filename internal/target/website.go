package target

type WebsiteTarget struct {
	Name    string
	Address string
	Safe    bool
}

func (t *WebsiteTarget) Check() (bool, error) {
	return true, nil
}
